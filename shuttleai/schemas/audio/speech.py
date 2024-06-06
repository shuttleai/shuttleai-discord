from pydantic import BaseModel


class AudioSpeech(BaseModel):
    url: str
    """The URL of the audio file."""


class AudioSpeechResponse(BaseModel):
    created: int
    """The Unix timestamp when the audio generation was created."""

    data: AudioSpeech
    """The generated audio file."""

    model: str
    """The model used to generate the audio file."""

    chars: int
    """The number of characters in the audio file."""

    expiresIn: int = 3600
    """The number of seconds before the audio file expires."""
