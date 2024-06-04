from pydantic import BaseModel


class AudioTranslationResponse(BaseModel):
    text: str
    """The translated/transcribed text."""
