from typing import List

from pydantic import BaseModel


class Image(BaseModel):
    url: str
    """The URL of the image."""

    def to_file(self, path: str) -> None:
        """Save the image to a file.

        Args:
            path (str): The path to save the image to.
        """
        import httpx

        response = httpx.get(self.url)
        with open(path, "wb") as file:
            file.write(response.content)

    def to_bytes(self) -> bytes:
        """Get the image as bytes.

        Returns:
            bytes: The image as bytes.
        """
        import httpx

        response = httpx.get(self.url)
        return response.content

    def show(self) -> None:
        """Show the image using pillow."""
        from io import BytesIO

        from PIL import Image as PILImage

        image = PILImage.open(BytesIO(self.to_bytes()))
        image.show()

    def __str__(self) -> str:
        return self.url


class ImagesGenerationResponse(BaseModel):
    created: int
    """The Unix timestamp when the image generation was created."""

    data: List[Image]
    """The generated image(s)."""

    @property
    def first_image(self) -> Image:
        return self.data[0]
