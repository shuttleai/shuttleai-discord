from enum import Enum
from typing import List, Optional, Union

from pydantic import BaseModel

from shuttleai.exceptions import ShuttleAIException
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


class ContentPartType(str, Enum):
    text = "text"
    image_url = "image_url"


class ToolCall(BaseModel):
    id: str = "call_null"
    type: ToolType = ToolType.function
    function: FunctionCall


class ToolChoice(str, Enum):
    auto: str = "auto"
    none: str = "none"


class ChatMessageContentPartText(BaseModel):
    type: ContentPartType = ContentPartType.text
    text: str


class ChatMessageContentPartImage(BaseModel):
    type: ContentPartType = ContentPartType.image_url
    image_url: str


class ChatMessage(BaseModel):
    role: str
    content: Optional[Union[str, List[Union[ChatMessageContentPartText, ChatMessageContentPartImage]]]] = None
    name: Optional[str] = None
    tool_calls: Optional[List[ToolCall]] = None
    # tool_call_id: Optional[str] = None


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

    @property
    def first_choice(self) -> ChatCompletionResponseStreamChoice:
        return self.choices[0]

    def print_chunk(self) -> None:
        try:
            print(f"Request ID: {self.id}")
            print(f"Model: {self.model}")
            print(f"Created: {self.created}")
            print(f"Usage: {self.usage}")
            for choice in self.choices:
                print(f"Index: {choice.index}")
                print(f"Delta: {choice.delta}")
                print(f"Finish Reason: {choice.finish_reason}")
        except Exception as e:
            raise ShuttleAIException(f"Error printing response: {e}") from e


class ChatCompletionResponseChoice(BaseModel):
    index: int
    message: ChatMessage
    finish_reason: Optional[FinishReason]


# class ShuttleAIMeta(BaseModel):
#     id: str
#     """The ID of the request."""

#     p: str
#     """The ID of the provider that processed the request.

#     The provider ID is semi-reliable, meaning upon VPS restarts, provider IDs may change;
#     however, they are guaranteed to remain the same for the duration of the VPS uptime.
#     (This can be useful for debugging/reporting purposes.)"""


class ChatCompletionResponse(BaseModel):
    id: str
    object: str
    created: int
    model: str
    choices: List[ChatCompletionResponseChoice]
    usage: UsageInfo

    @property
    def cost(self) -> float:
        return self.usage.total_charged
    # x_sai: Annotated[
    #     ShuttleAIMeta,
    #     Field(
    #         alias="x-sai",
    #         alias_priority=1,
    #         examples=[{"id": "req_123abc", "p": "p_123abc"}],
    #     ),
    # ]

    # @property
    # def xsai(self) -> ShuttleAIMeta:
    #     return self.x_sai

    # @property
    # def meta(self) -> ShuttleAIMeta:
    #     return self.x_sai

    # @property
    # def provider(self) -> str:
    #     return self.x_sai.p

    # @property
    # def provider_id(self) -> str:
    #     return self.x_sai.p

    # @property
    # def request_id(self) -> str:
    #     return self.x_sai.id

    @property
    def first_choice(self) -> ChatCompletionResponseChoice:
        return self.choices[0]

    def print(self) -> None:
        try:
            # print(f"Request ID: {self.request_id}")
            # print(f"Provider ID: {self.provider_id}")
            print(f"Model: {self.model}")
            print(f"Created: {self.created}")
            print(f"Usage: {self.usage}")
            for choice in self.choices:
                print(f"Index: {choice.index}")
                print(f"Message: {choice.message}")
                print(f"Finish Reason: {choice.finish_reason}")
        except Exception as e:
            raise ShuttleAIException(f"Error printing response: {e}") from e
