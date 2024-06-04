from typing import Any, AsyncIterable, AsyncIterator, Dict, Iterator, Type

from pydantic import BaseModel

from shuttleai.client.base import ClientBase
from shuttleai.exceptions import ShuttleAIException


class BaseResource:
    def __init__(self, client: ClientBase):
        self._client = client


class SyncResource(BaseResource):
    def _stream_response(
        self, response: Iterator[Dict[str, Any]], response_cls: Type[BaseModel]
    ) -> Iterator[BaseModel]:
        for json_streamed_response in response:
            yield response_cls(**json_streamed_response)

    def _no_stream_response(
        self, response: Iterator[Dict[str, Any]], response_cls: Type[BaseModel]
    ) -> BaseModel:
        for resp in response:
            return response_cls(**resp)
        raise ShuttleAIException("No response received")

    def handle_request(
        self,
        method: str,
        endpoint: str,
        request_data: Dict[str, Any],
        response_cls: Type[BaseModel],
        stream: bool = False,
    ) -> Any:
        # assert issubclass(response_cls, BaseModel)
        response = self._client._request(  # type: ignore
            method=method,
            json=request_data,
            path=endpoint,
            stream=stream,
        )
        if stream:
            return self._stream_response(response, response_cls)
        else:
            return self._no_stream_response(response, response_cls)


class AsyncResource(BaseResource):
    async def _stream_response(
        self, response: AsyncIterator[Dict[str, Any]], response_cls: Type[BaseModel]
    ) -> AsyncIterable[BaseModel]:
        async for json_streamed_response in response:
            yield response_cls(**json_streamed_response)

    async def _no_stream_response(
        self, response: AsyncIterator[Dict[str, Any]], response_cls: Type[BaseModel]
    ) -> BaseModel:
        async for resp in response:
            return response_cls(**resp)
        raise ShuttleAIException("No response received")

    async def handle_request(
        self,
        method: str,
        endpoint: str,
        request_data: Dict[str, Any],
        response_cls: Type[BaseModel],
        stream: bool = False,
    ) -> Any:
        assert issubclass(response_cls, BaseModel)
        response = self._client._request(  # type: ignore
            method=method,
            json=request_data,
            path=endpoint,
            stream=stream,
        )
        if stream:
            return self._stream_response(response, response_cls)
        else:
            return await self._no_stream_response(response, response_cls)
