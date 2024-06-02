import logging
import os
from abc import ABC
from typing import Any, Dict, List, Optional, Union

import orjson

from shuttleai import __version__
from shuttleai.exceptions import (
    ShuttleAIException,
)
from shuttleai.schemas.chat_completion import ChatMessage, Function, ToolChoice


class ClientBase(ABC):
    def __init__(
        self,
        base_url: str,
        api_key: Optional[str] = None,
        timeout: int = 120,
    ):
        self._timeout = timeout

        if api_key is None:
            api_key = os.getenv("SHUTTLEAI_API_KEY")
        if api_key is None:
            raise ShuttleAIException("API key not provided. Please set SHUTTLEAI_API_KEY environment variable.")
        self._api_key = api_key
        self._base_url = base_url
        self._logger = logging.getLogger(__name__)

        if "shuttleai.app" not in self._base_url:
            self._logger.warning(
                "You are using a non-ShuttleAI URL. \
                    This is not recommended and may lead to personal data leaks. \
                        Be cautious."
            )
        else:
            self._default_model = "shuttle-2-turbo"

        self._version = __version__

    def _parse_tools(self, tools: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        parsed_tools: List[Dict[str, Any]] = []
        for tool in tools:
            if tool["type"] == "function":
                parsed_function = {}
                parsed_function["type"] = tool["type"]
                if isinstance(tool["function"], Function):
                    parsed_function["function"] = tool["function"].model_dump(exclude_none=True)
                else:
                    parsed_function["function"] = tool["function"]

                parsed_tools.append(parsed_function)

        return parsed_tools

    def _parse_tool_choice(self, tool_choice: Union[str, ToolChoice]) -> str:
        if isinstance(tool_choice, ToolChoice):
            return tool_choice.value
        return tool_choice

    def _parse_messages(self, messages: List[Any]) -> List[Dict[str, Any]]:
        parsed_messages: List[Dict[str, Any]] = []
        for message in messages:
            if isinstance(message, ChatMessage):
                parsed_messages.append(message.model_dump(exclude_none=True))
            else:
                parsed_messages.append(message)

        return parsed_messages

    def _make_completion_request(
        self,
        prompt: str,
        model: Optional[str] = None,
        suffix: Optional[str] = None,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        top_p: Optional[float] = None,
        stop: Optional[List[str]] = None,
        stream: Optional[bool] = False,
    ) -> Dict[str, Any]:
        request_data: Dict[str, Any] = {
            "prompt": prompt,
            "suffix": suffix,
            "model": model,
            "stream": stream,
        }

        if stop is not None:
            request_data["stop"] = stop

        if model is not None:
            request_data["model"] = model
        else:
            if self._default_model is None:
                raise ShuttleAIException(message="model must be provided")
            request_data["model"] = self._default_model

        request_data.update(
            self._build_sampling_params(
                temperature=temperature, max_tokens=max_tokens, top_p=top_p
            )
        )

        self._logger.debug(f"Completion request: {request_data}")

        return request_data

    def _build_sampling_params(
        self,
        max_tokens: Optional[int],
        temperature: Optional[float],
        top_p: Optional[float],
    ) -> Dict[str, Any]:
        params = {}
        if temperature is not None:
            params["temperature"] = temperature
        if max_tokens is not None:
            params["max_tokens"] = max_tokens
        if top_p is not None:
            params["top_p"] = top_p
        return params

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

        if model is not None:
            request_data["model"] = model
        else:
            if self._default_model is None:
                raise ShuttleAIException(message="model must be provided")
            request_data["model"] = self._default_model

        request_data.update(
            self._build_sampling_params(
                temperature=temperature, max_tokens=max_tokens, top_p=top_p
            )
        )

        if tools is not None:
            request_data["tools"] = self._parse_tools(tools)
        if stream is not None:
            request_data["stream"] = stream

        if tool_choice is not None:
            request_data["tool_choice"] = self._parse_tool_choice(tool_choice)

        self._logger.debug(f"Chat request: {request_data}")

        return request_data

    def _process_line(self, line: str | bytes) -> Optional[Dict[str, Any]]:
        line = line.encode("utf-8") if isinstance(line, str) else line
        if line.startswith(b"data: "):
            line = line[6:].strip()
            if line != b"[DONE]":
                json_streamed_response: Dict[str, Any] = orjson.loads(line)
                return json_streamed_response
        return None
