from typing import Literal, Optional, Union

from shuttleai.resources.common import AsyncResource, SyncResource
from shuttleai.schemas.etc.insults import InsultResponse


class AsyncInsults(AsyncResource):
    async def generate(
        self,
        model: Optional[Union[str, Literal["insult-1"]]] = "insult-1",
    ) -> InsultResponse:

        return await self.handle_request(  # type: ignore
            method="get",
            endpoint=f"v1/insults?key={self._client.api_key}&model={model}",
            request_data=None,
            response_cls=InsultResponse,
        )


class Insults(SyncResource):
    def generate(
        self,
        model: Optional[Union[str, Literal["insult-1"]]] = "insult-1",
    ) -> InsultResponse:

        return self.handle_request(  # type: ignore
            method="get",
            endpoint=f"v1/insults?key={self._client.api_key}&model={model}",
            request_data=None,
            response_cls=InsultResponse,
        )
