from typing import List

from pydantic import BaseModel


class Image(BaseModel):
    url: str
    """The URL of the image."""


class ImagesGenerationResponse(BaseModel):
    created: int
    """The Unix timestamp when the image generation was created."""

    data: List[Image]
    """The generated image(s)."""
