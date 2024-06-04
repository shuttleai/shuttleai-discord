from typing import Optional

from pydantic import BaseModel


class SupportsTools(BaseModel):
    regular: bool
    """Whether the model supports regular tool calling."""

    streamed: bool
    """Whether the model supports streamed tool calling."""

    parallel: bool
    """Whether the model supports parallel tool calling."""


class SupportsMaxTokens(BaseModel):
    input: int
    """The maximum number of tokens that can be input to the model."""

    output: int
    """The maximum number of tokens that can be output from the model."""


class Capabilities(BaseModel):
    supports_tools: Optional[SupportsTools] = None
    """The tool calling capabilities of the model."""

    supports_max_tokens: Optional[SupportsMaxTokens] = None
    """The maximum token capabilities of the model."""

    supports_image_input: bool
    """Whether the model supports image input."""

    supports_audio_input: bool
    """Whether the model supports audio input."""
