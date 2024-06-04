from pydantic import BaseModel


class AudioTranscriptionResponse(BaseModel):
    text: str
    """The transcribed text."""
