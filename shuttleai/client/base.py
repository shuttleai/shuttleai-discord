import logging
import os
from abc import ABC
from typing import Any, Dict, List, Optional, Union

import orjson

from shuttleai import __version__
from shuttleai._types import TimeoutTypes
from shuttleai.exceptions import ShuttleAIException
from shuttleai.schemas.chat_completion import ChatMessage, Function, ToolChoice


class ClientBase(ABC):  # noqa: B024

    _timeout: TimeoutTypes
    _api_key: Optional[str]
    _base_url: str
    _logger: logging.Logger
    _default_chat_model: str
    _default_image_model: str
    _version: str

    def __init__(
        self,
        base_url: str,
        api_key: Optional[str] = None,
        timeout: TimeoutTypes = 120.0,
    ):
        self._timeout = timeout
        self._api_key = api_key or os.getenv("SHUTTLEAI_API_KEY")
        if not self._api_key:
            raise ShuttleAIException("API key not provided. Please set SHUTTLEAI_API_KEY environment variable.")
        self._base_url = base_url
        self._logger = logging.getLogger(__name__)
        self._default_chat_model = "shuttle-2-turbo"
        self._default_image_model = "sdxl"
        self._version = __version__

        if "shuttleai.app" not in self._base_url:
            if "api.openai.com" not in self._base_url:
                self._logger.warning(
                    "You are using an **unofficial, unverified** non-ShuttleAI URL. \
                    This is not recommended and may lead to malfunctions. \
                    Your data could be at risk since you are using a 3rd party. \
                    Please use the official ShuttleAI API URL: https://api.shuttleai.app/v1"
                )
            else:
                self._logger.warning(
                    "You are using the official, verified OpenAI API URL. \
                    This library is not meant to replace the OpenAI SDK. \
                    If you wish to use the OpenAI API, consider using their SDK respectively. \
                    Otherwise, please use the official ShuttleAI API URL: https://api.shuttleai.app/v1"
                )
            self._default_chat_model = "gpt-3.5-turbo"
            self._default_image_model = "dall-e-2"

        self._logger.info(f"ShuttleAI API client initialized with base URL: {self._base_url}")

    def _build_sampling_params(
        self,
        max_tokens: Optional[int],
        temperature: Optional[float],
        top_p: Optional[float],
    ) -> Dict[str, Any]:
        return {
            k: v for k, v in {
                "temperature": temperature, "max_tokens": max_tokens, "top_p": top_p
            }.items() if v is not None
        }

    def _parse_tools(self, tools: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        return [
            {"type": tool["type"], "function": tool["function"].model_dump(exclude_none=True)
             if isinstance(tool["function"], Function) else tool["function"]}
            for tool in tools if tool["type"] == "function"
        ]

    def _parse_tool_choice(self, tool_choice: Union[str, ToolChoice]) -> str:
        return tool_choice.value if isinstance(tool_choice, ToolChoice) else tool_choice

    def _parse_messages(self, messages: List[Any]) -> List[Dict[str, Any]]:
        return [
            message.model_dump(exclude_none=True) if isinstance(message, ChatMessage) else message
            for message in messages
        ]

    def _make_request(self, endpoint: str, request_data: Dict[str, Any]) -> Dict[str, Any]:
        if "model" not in request_data:
            request_data["model"] = getattr(self, f"_default_{endpoint}_model")
        self._logger.debug(f"{endpoint.capitalize()} request: {request_data}")
        return request_data

    def _make_chat_request(
        self,
        messages: List[Any],
        model: Optional[str] = None,
        tools: Optional[List[Dict[str, Any]]] = None,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        top_p: Optional[float] = None,
        stream: Optional[bool] = None,
        tool_choice: Optional[Union[str, ToolChoice]] = None,
    ) -> Dict[str, Any]:
        request_data: Dict[str, Any] = {
            "messages": self._parse_messages(messages),
        }
        if model:
            request_data["model"] = model
        if tools:
            request_data["tools"] = self._parse_tools(tools)
        if tool_choice:
            request_data["tool_choice"] = self._parse_tool_choice(tool_choice)
        if stream:
            request_data["stream"] = stream
        request_data.update(self._build_sampling_params(max_tokens, temperature, top_p))
        return self._make_request("chat", request_data)

    def _make_image_request(
        self,
        prompt: str,
        model: Optional[str] = None
    ) -> Dict[str, Any]:
        request_data: Dict[str, Any] = {
            "prompt": prompt,
        }
        if model:
            request_data["model"] = model
        return self._make_request("image", request_data)

    def _process_line(self, line: Union[str, bytes]) -> Optional[Dict[str, Any] | Any]:
        line = line.encode("utf-8") if isinstance(line, str) else line
        if line.startswith(b"data: "):
            line = line[6:].strip()
            if line != b"[DONE]":
                return orjson.loads(line)
        return None
