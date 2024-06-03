from typing import List

from pydantic import BaseModel


class Image(BaseModel):

    url: str
    """The URL of the image."""


ListImageChoicesData = List[Image]


class ImagesGenerationResponse(BaseModel):

    created: int
    """The Unix timestamp when the image generation was created."""

    data: ListImageChoicesData
    """The generated image(s)."""
