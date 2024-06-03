from typing import (
    Any,
    AsyncIterable,
    Dict,
    Iterable,
    List,
    Literal,
    Optional,
    Union,
    overload,
)

from shuttleai.client.base import ClientBase
from shuttleai.resources._resource import AsyncResource, SyncResource
from shuttleai.schemas.chat_completion import (
    ChatCompletionResponse,
    ChatCompletionStreamResponse,
    ChatMessage,
    ToolChoice,
)


class AsyncCompletions(AsyncResource):
    @overload
    async def create(  # type: ignore
        self,
        messages: Union[List[ChatMessage], List[Dict[str, Any]]],
        model: Optional[str] = None,
        tools: Optional[List[Dict[str, Any]]] = None,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        top_p: Optional[float] = None,
        tool_choice: Optional[Union[str, ToolChoice]] = None,
        stream: Literal[False] = False,
    ) -> ChatCompletionResponse: ...

    @overload
    async def create(
        self,
        messages: Union[List[ChatMessage], List[Dict[str, Any]]],
        model: Optional[str] = None,
        tools: Optional[List[Dict[str, Any]]] = None,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        top_p: Optional[float] = None,
        tool_choice: Optional[Union[str, ToolChoice]] = None,
        stream: Literal[True] = True,
    ) -> AsyncIterable[ChatCompletionStreamResponse]: ...

    async def create(
        self,
        messages: Union[List[ChatMessage], List[Dict[str, Any]]],
        model: Optional[str] = None,
        tools: Optional[List[Dict[str, Any]]] = None,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        top_p: Optional[float] = None,
        tool_choice: Optional[Union[str, ToolChoice]] = None,
        stream: bool = False,
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

        return await self.handle_request(  # type: ignore
            method="post",
            endpoint="v1/chat/completions",
            request_data=request,
            response_cls=ChatCompletionStreamResponse if stream else ChatCompletionResponse,  # type: ignore
            stream=stream,
        )


class SyncCompletions(SyncResource):
    @overload
    def create(  # type: ignore
        self,
        messages: Union[List[ChatMessage], List[Dict[str, Any]]],
        model: Optional[str] = None,
        tools: Optional[List[Dict[str, Any]]] = None,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        top_p: Optional[float] = None,
        tool_choice: Optional[Union[str, ToolChoice]] = None,
        stream: Literal[False] = False,
    ) -> ChatCompletionResponse: ...

    @overload
    def create(
        self,
        messages: Union[List[ChatMessage], List[Dict[str, Any]]],
        model: Optional[str] = None,
        tools: Optional[List[Dict[str, Any]]] = None,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        top_p: Optional[float] = None,
        tool_choice: Optional[Union[str, ToolChoice]] = None,
        stream: Literal[True] = True,
    ) -> Iterable[ChatCompletionStreamResponse]: ...

    def create(
        self,
        messages: Union[List[ChatMessage], List[Dict[str, Any]]],
        model: Optional[str] = None,
        tools: Optional[List[Dict[str, Any]]] = None,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        top_p: Optional[float] = None,
        tool_choice: Optional[Union[str, ToolChoice]] = None,
        stream: bool = False,
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

        return self.handle_request(  # type: ignore
            method="post",
            endpoint="v1/chat/completions",
            request_data=request,
            response_cls=ChatCompletionStreamResponse if stream else ChatCompletionResponse,  # type: ignore
            stream=stream,
        )


class AsyncChat:
    def __init__(self, client: ClientBase):
        self._completions: Optional[AsyncCompletions] = None
        self._client = client

    @property
    def completions(self) -> AsyncCompletions:
        if self._completions is None:
            self._completions = AsyncCompletions(self._client)
        return self._completions


class Chat:
    def __init__(self, client: ClientBase):
        self._completions: Optional[SyncCompletions] = None
        self._client = client

    @property
    def completions(self) -> SyncCompletions:
        if self._completions is None:
            self._completions = SyncCompletions(self._client)
        return self._completions
