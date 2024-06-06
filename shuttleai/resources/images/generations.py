from functools import cached_property
from typing import Generic, Optional, Type, TypeVar

from shuttleai.client.base import ClientBase
from shuttleai.resources.common import AsyncResource, SyncResource, T
from shuttleai.schemas.images.generations import ImagesGenerationResponse


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


GenerationsType = TypeVar("GenerationsType", SyncGenerations, AsyncGenerations)


class BaseImages(Generic[T, GenerationsType]):
    _client: T
    _generations_class: Type[GenerationsType]
    _generations: Optional[GenerationsType]

    def __init__(self, client: T, generations_class: Type[GenerationsType]) -> None:
        self._client = client
        self._generations_class = generations_class
        self._generations = None

    @cached_property
    def generations(self) -> GenerationsType:
        if self._generations is None:
            self._generations = self._generations_class(self._client)
        return self._generations


class Images(BaseImages[ClientBase, SyncGenerations]):
    def __init__(self, client: ClientBase) -> None:
        super().__init__(client, SyncGenerations)


class AsyncImages(BaseImages[ClientBase, AsyncGenerations]):
    def __init__(self, client: ClientBase) -> None:
        super().__init__(client, AsyncGenerations)
