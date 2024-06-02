from typing import Any, AsyncIterable, Dict, List, Literal, Optional, Union, overload

from shuttleai.client.base import ClientBase
from shuttleai.exceptions import ShuttleAIException
from shuttleai.schemas.chat_completion import (
    ChatCompletionResponse,
    ChatCompletionStreamResponse,
    ChatMessage,
    ToolChoice,
)


class Completions:
    def __init__(self, client: ClientBase):
        self._client = client

    @overload
    async def create(
        self,
        messages: List[Union[ChatMessage, Dict[str, Any]]],
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
        messages: List[Union[ChatMessage, Dict[str, Any]]],
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
        messages: List[Union[ChatMessage, Dict[str, Any]]],
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

class Chat:
    def __init__(self, client: ClientBase):
        self.completions = Completions(client)
