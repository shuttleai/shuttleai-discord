from typing import Any, AsyncIterable, Dict, Iterable, List, Literal, Optional, Union, overload

from shuttleai.client.base import ClientBase
from shuttleai.exceptions import ShuttleAIException
from shuttleai.schemas.chat_completion import (
    ChatCompletionResponse,
    ChatCompletionStreamResponse,
    ChatMessage,
    ToolChoice,
)


class BaseCompletions:
    def __init__(self, client: ClientBase):
        self._client = client


class AsyncCompletions(BaseCompletions):
    @overload
    async def create(
        self,
        messages: List[ChatMessage] | List[Dict[str, Any]],
        model: Optional[str] = None,
        tools: Optional[List[Dict[str, Any]]] = None,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        top_p: Optional[float] = None,
        tool_choice: Optional[Union[str, ToolChoice]] = None,
        stream: Literal[False] = False
    ) -> ChatCompletionResponse:
        ...

    @overload
    async def create(
        self,
        messages: List[ChatMessage] | List[Dict[str, Any]],
        model: Optional[str] = None,
        tools: Optional[List[Dict[str, Any]]] = None,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        top_p: Optional[float] = None,
        tool_choice: Optional[Union[str, ToolChoice]] = None,
        stream: Literal[True] = True
    ) -> AsyncIterable[ChatCompletionStreamResponse]:
        ...

    async def create(
        self,
        messages: List[ChatMessage] | List[Dict[str, Any]],
        model: Optional[str] = None,
        tools: Optional[List[Dict[str, Any]]] = None,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        top_p: Optional[float] = None,
        tool_choice: Optional[Union[str, ToolChoice]] = None,
        stream: bool = False
    ) -> Union[ChatCompletionResponse, AsyncIterable[ChatCompletionStreamResponse]]:
        request = self._client._make_chat_request(
            messages,
            model,
            tools=tools,
            temperature=temperature,
            max_tokens=max_tokens,
            top_p=top_p,
            stream=stream,
            tool_choice=tool_choice,
        )

        if stream:
            response = self._client._request("post", request, "v1/chat/completions", stream=True)
            return (ChatCompletionStreamResponse(**json_streamed_response) async for json_streamed_response in response)
        else:
            single_response = self._client._request("post", request, "v1/chat/completions")
            async for response in single_response:
                return ChatCompletionResponse(**response)

            raise ShuttleAIException("No response received")


class SyncCompletions(BaseCompletions):
    @overload
    def create(
        self,
        # messages: List[Union[ChatMessage, Dict[str, Any]]], # original
        messages: List[ChatMessage] | List[Dict[str, Any]], # modified
        model: Optional[str] = None,
        tools: Optional[List[Dict[str, Any]]] = None,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        top_p: Optional[float] = None,
        tool_choice: Optional[Union[str, ToolChoice]] = None,
        stream: Literal[False] = False
    ) -> ChatCompletionResponse:
        ...

    @overload
    def create(
        self,
        messages: List[ChatMessage] | List[Dict[str, Any]],
        model: Optional[str] = None,
        tools: Optional[List[Dict[str, Any]]] = None,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        top_p: Optional[float] = None,
        tool_choice: Optional[Union[str, ToolChoice]] = None,
        stream: Literal[True] = True
    ) -> Iterable[ChatCompletionStreamResponse]:
        ...

    def create(
        self,
        messages: List[ChatMessage] | List[Dict[str, Any]],
        model: Optional[str] = None,
        tools: Optional[List[Dict[str, Any]]] = None,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        top_p: Optional[float] = None,
        tool_choice: Optional[Union[str, ToolChoice]] = None,
        stream: bool = False
    ) -> Union[ChatCompletionResponse, Iterable[ChatCompletionStreamResponse]]:
        request = self._client._make_chat_request(
            messages,
            model,
            tools=tools,
            temperature=temperature,
            max_tokens=max_tokens,
            top_p=top_p,
            stream=stream,
            tool_choice=tool_choice,
        )

        if stream:
            response = self._client._request("post", request, "v1/chat/completions", stream=True)
            return (ChatCompletionStreamResponse(**json_streamed_response) for json_streamed_response in response)
        else:
            single_response = self._client._request("post", request, "v1/chat/completions")
            for response in single_response:
                return ChatCompletionResponse(**response)

            raise ShuttleAIException("No response received")


class Chat:
    def __init__(self, client: ClientBase, async_mode: bool = True):
        # async_mode: temp fix since asyncio.iscoroutinefunction works but not in this context
        # TODO: dynamic fix
        if async_mode:
            self.completions = AsyncCompletions(client)
        else:
            self.completions = SyncCompletions(client)
