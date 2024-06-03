from typing import Optional

from shuttleai.client.base import ClientBase
from shuttleai.resources._resource import AsyncResource, SyncResource
from shuttleai.schemas.images_generations import ImagesGenerationResponse


class AsyncGenerations(AsyncResource):
    async def generate(
        self,
        prompt: str,
        model: Optional[str] = None,
    ) -> ImagesGenerationResponse:
        request = self._client._make_image_request(
            prompt,
            model,
        )

        return await self.handle_request(  # type: ignore
            method="post",
            endpoint="v1/images/generations",
            request_data=request,
            response_cls=ImagesGenerationResponse,
        )


class SyncGenerations(SyncResource):
    def generate(
        self,
        prompt: str,
        model: Optional[str] = None,
    ) -> ImagesGenerationResponse:
        request = self._client._make_image_request(
            prompt,
            model,
        )

        return self.handle_request(  # type: ignore
            method="post",
            endpoint="v1/images/generations",
            request_data=request,
            response_cls=ImagesGenerationResponse,
        )


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
