from typing import Optional

from shuttleai.client.base import ClientBase
from shuttleai.exceptions import ShuttleAIException
from shuttleai.schemas.images_generations import ImagesGenerationResponse


class BaseImages:
    def __init__(self, client: ClientBase):
        self._client = client


class AsyncImages(BaseImages):
    async def generate(
        self,
        prompt: str,
        model: Optional[str] = None,
    ) -> ImagesGenerationResponse:
        request = self._client._make_image_request(
            prompt,
            model,
        )

        single_response = self._client._request("post", request, "v1/images/generations")

        async for response in single_response:
            return ImagesGenerationResponse(**response)

        raise ShuttleAIException("No response received")


class SyncImages(BaseImages):
        def generate(
            self,
            prompt: str,
            model: Optional[str] = None,
        ) -> ImagesGenerationResponse:
            request = self._client._make_image_request(
                prompt,
                model,
            )

            single_response = self._client._request("post", request, "v1/images/generations")

            for response in single_response:
                return ImagesGenerationResponse(**response)

            raise ShuttleAIException("No response received")


class Images:
    def __init__(self, client: ClientBase, async_mode: bool = True):
        if async_mode:
            self._client = AsyncImages(client)
        else:
            self._client = SyncImages(client)
