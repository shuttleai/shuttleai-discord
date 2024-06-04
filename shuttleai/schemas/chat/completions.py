from enum import Enum
from typing import Annotated, List, Optional, Union

from pydantic import BaseModel, Field

from shuttleai.schemas.common import UsageInfo


class Function(BaseModel):
    name: str
    description: str
    parameters: dict


class ToolType(str, Enum):
    function = "function"


class FunctionCall(BaseModel):
    name: str
    arguments: str


class ToolCall(BaseModel):
    id: str = "call_null"
    type: ToolType = ToolType.function
    function: FunctionCall


class ToolChoice(str, Enum):
    auto: str = "auto"
    none: str = "none"


class ChatMessage(BaseModel):
    role: str
    content: Optional[Union[str, List[str]]] = None
    name: Optional[str] = None
    tool_calls: Optional[List[ToolCall]] = None
    tool_call_id: Optional[str] = None


class DeltaMessage(BaseModel):
    role: Optional[str] = None
    content: Optional[str] = None
    tool_calls: Optional[List[ToolCall]] = None


class FinishReason(str, Enum):
    stop = "stop"
    length = "length"
    tool_calls = "tool_calls"


class ChatCompletionResponseStreamChoice(BaseModel):
    index: int
    delta: DeltaMessage
    finish_reason: Optional[FinishReason]


class ChatCompletionStreamResponse(BaseModel):
    id: str
    model: str
    choices: List[ChatCompletionResponseStreamChoice]
    created: Optional[int] = None
    object: Optional[str] = None
    usage: Optional[UsageInfo] = None


class ChatCompletionResponseChoice(BaseModel):
    index: int
    message: ChatMessage
    finish_reason: Optional[FinishReason]


class ShuttleAIMeta(BaseModel):
    id: str
    """The ID of the request."""

    p: str
    """The ID of the provider that processed the request.

    The provider ID is semi-reliable, meaning upon VPS restarts, provider IDs may change."""


class ChatCompletionResponse(BaseModel):
    id: str
    object: str
    created: int
    model: str
    choices: List[ChatCompletionResponseChoice]
    usage: UsageInfo
    x_sai: Annotated[
        ShuttleAIMeta,
        Field(
            alias="x-sai",
            alias_priority=1,
            examples=[{"id": "req_123abc", "p": "p_123abc"}],
        ),
    ]

    @property
    def xsai(self) -> ShuttleAIMeta:
        return self.x_sai

    @property
    def meta(self) -> ShuttleAIMeta:
        return self.x_sai

    @property
    def provider(self) -> str:
        return self.x_sai.p

    @property
    def provider_id(self) -> str:
        return self.x_sai.p

    @property
    def request_id(self) -> str:
        return self.x_sai.id
