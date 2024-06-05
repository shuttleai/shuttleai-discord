from typing import (
    Any,
    AsyncIterable,
    Dict,
    Generic,
    Iterable,
    List,
    Literal,
    Optional,
    Type,
    TypeVar,
    Union,
    overload,
)

from shuttleai.client.base import ClientBase
from shuttleai.helpers import cached_property
from shuttleai.resources.common import AsyncResource, SyncResource, T
from shuttleai.schemas.chat.completions import (
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


CompletionsType = TypeVar("CompletionsType", SyncCompletions, AsyncCompletions)

class BaseChat(Generic[T, CompletionsType]):
    _client: T
    _completions_class: Type[CompletionsType]

    def __init__(self, client: T, completions_class: Type[CompletionsType]) -> None:
        self._client = client
        self._completions_class = completions_class

    @cached_property
    def completions(self) -> CompletionsType:
        return self._completions_class(self._client)


class Chat(BaseChat[ClientBase, SyncCompletions]):
    def __init__(self, client: ClientBase) -> None:
        super().__init__(client, SyncCompletions)

class AsyncChat(BaseChat[ClientBase, AsyncCompletions]):
    def __init__(self, client: ClientBase) -> None:
        super().__init__(client, AsyncCompletions)
