from typing import Literal, Optional, Union

from shuttleai.resources.common import AsyncResource, SyncResource
from shuttleai.schemas.etc.web_search import WebSearchResponse


class AsyncWeb(AsyncResource):
    async def search(
        self,
        query: str,
        limit: int = 3,
        model: Optional[Union[str, Literal["search-ddg", "search-google"]]] = "search-ddg",
    ) -> WebSearchResponse:
        request = {"query": query, "limit": limit, "model": model}
        return await self.handle_request(  # type: ignore
            method="post",
            endpoint="/web-search",
            request_data=request,
            response_cls=WebSearchResponse,
        )


class Web(SyncResource):
    def search(
        self,
        query: str,
        limit: int = 3,
        model: Optional[Union[str, Literal["search-ddg", "search-google"]]] = "search-ddg",
    ) -> WebSearchResponse:
        request = {"query": query, "limit": limit, "model": model}
        return self.handle_request(  # type: ignore
            method="post",
            endpoint="/web-search",
            request_data=request,
            response_cls=WebSearchResponse,
        )
