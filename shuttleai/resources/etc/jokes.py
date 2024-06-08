from typing import Literal, Optional, Union

from shuttleai.resources.common import AsyncResource, SyncResource
from shuttleai.schemas.etc.jokes import JokeResponse


class AsyncJokes(AsyncResource):
    async def generate(
        self,
        model: Optional[Union[str, Literal["joke-1"]]] = "joke-1",
    ) -> JokeResponse:

        return await self.handle_request(  # type: ignore
            method="get",
            endpoint=f"v1/jokes?key={self._client.api_key}&model={model}",
            request_data=None,
            response_cls=JokeResponse,
        )


class Jokes(SyncResource):
    def generate(
        self,
        model: Optional[Union[str, Literal["joke-1"]]] = "joke-1",
    ) -> JokeResponse:

        return self.handle_request(  # type: ignore
            method="get",
            endpoint=f"v1/jokes?key={self._client.api_key}&model={model}",
            request_data=None,
            response_cls=JokeResponse,
        )
