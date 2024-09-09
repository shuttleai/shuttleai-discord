from typing import Literal, Optional, Union

from shuttleai.resources.common import AsyncResource, SyncResource
from shuttleai.schemas.embeddings import EmbeddingResponse


class AsyncEmbeddings(AsyncResource):
    async def create(
        self,
        input: str,
        model: Optional[
            Union[str, Literal["text-embedding-3-small", "text-embedding-3-large"]]
        ] = "text-embedding-3-large",
    ) -> EmbeddingResponse:
        request = {"input": input, "model": model}

        return await self.handle_request(  # type: ignore
            method="post",
            endpoint="/embeddings",
            request_data=request,
            response_cls=EmbeddingResponse,
        )


class Embeddings(SyncResource):
    def create(
        self,
        input: str,
        model: Optional[
            Union[str, Literal["text-embedding-3-small", "text-embedding-3-large"]]
        ] = "text-embedding-3-large",
    ) -> EmbeddingResponse:
        request = {"input": input, "model": model}

        return self.handle_request(  # type: ignore
            method="post",
            endpoint="/embeddings",
            request_data=request,
            response_cls=EmbeddingResponse,
        )
