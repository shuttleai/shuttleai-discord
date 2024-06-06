from typing import Literal, Optional, Union

from shuttleai.resources.common import AsyncResource, SyncResource
from shuttleai.schemas.moderations import ModerationResponse


class AsyncModerations(AsyncResource):
    async def create(
        self,
        input: str,
        model: Optional[
            Union[str, Literal["text-moderation-latest", "text-moderation-stable"]]
            ] = "text-moderation-stable",
    ) -> ModerationResponse:
        request = {"input": input, "model": model}

        return await self.handle_request(  # type: ignore
            method="post",
            endpoint="v1/moderations",
            request_data=request,
            response_cls=ModerationResponse,
        )


class Moderations(SyncResource):
    def create(
        self,
        input: str,
        model: Optional[
            Union[str, Literal["text-moderation-latest", "text-moderation-stable"]]
            ] = "text-moderation-stable",
    ) -> ModerationResponse:
        request = {"input": input, "model": model}

        return self.handle_request(  # type: ignore
            method="post",
            endpoint="v1/moderations",
            request_data=request,
            response_cls=ModerationResponse,
        )
