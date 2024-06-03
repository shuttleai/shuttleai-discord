from typing import Optional

from shuttleai.client.base import ClientBase
from shuttleai.exceptions import ShuttleAIException
from shuttleai.schemas.images_generations import ImagesGenerationResponse


class BaseGenerations:
    def __init__(self, client: ClientBase):
        self._client = client


class AsyncGenerations(BaseGenerations):
    async def generate(
        self,
        prompt: str,
        model: Optional[str] = None,
    ) -> ImagesGenerationResponse:
        request = self._client._make_image_request(
            prompt,
            model,
        )

        single_response = self._client._request(
            "post", request, "v1/images/generations"
        )

        async for response in single_response:
            return ImagesGenerationResponse(**response)

        raise ShuttleAIException("No response received")


class SyncGenerations(BaseGenerations):
    def generate(
        self,
        prompt: str,
        model: Optional[str] = None,
    ) -> ImagesGenerationResponse:
        request = self._client._make_image_request(
            prompt,
            model,
        )

        single_response = self._client._request(
            "post", request, "v1/images/generations"
        )

        for response in single_response:
            return ImagesGenerationResponse(**response)

        raise ShuttleAIException("No response received")


class Images:
    def __init__(self, client: ClientBase):
        self._generations: Optional[SyncGenerations] = None
        self._client = client

    @property
    def generations(self) -> SyncGenerations:
        if self._generations is None:
            self._generations = SyncGenerations(self._client)
        return self._generations


class AsyncImages:
    def __init__(self, client: ClientBase):
        self._generations: Optional[AsyncGenerations] = None
        self._client = client

    @property
    def generations(self) -> AsyncGenerations:
        if self._generations is None:
            self._generations = AsyncGenerations(self._client)
        return self._generations
