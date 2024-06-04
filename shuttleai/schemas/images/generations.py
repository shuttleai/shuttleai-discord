from typing import List

from pydantic import BaseModel


class Image(BaseModel):
    url: str
    """The URL of the image."""


Images = List[Image]


class ImagesGenerationResponse(BaseModel):
    created: int
    """The Unix timestamp when the image generation was created."""

    data: Images
    """The generated image(s)."""
