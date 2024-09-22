import posixpath
from typing import Any, AsyncIterable, AsyncIterator, Dict, Literal, Mapping, Optional, Type, Union, overload

import aiohttp
import orjson
import pydantic_core
from aiofiles import open as aopen
from aiohttp import ClientTimeout

from shuttleai import resources
from shuttleai._types import DEFAULT_AIOTTP_TIMEOUT, AIOHTTPTimeoutTypes
from shuttleai.client.base import ClientBase
from shuttleai.exceptions import (
    ShuttleAIAPIException,
    ShuttleAIAPIStatusException,
    ShuttleAIConnectionException,
    ShuttleAIException,
)
from shuttleai.schemas.chat.completions import ChatCompletionResponse, ChatCompletionStreamResponse
from shuttleai.schemas.models.models import (
    BaseModelCard,
    ListModelsResponse,
    ListVerboseModelsResponse,
    ProxyCard,
)


class AsyncShuttleAI(ClientBase):
    """
    Asynchronous wrapper for the ShuttleAI API
    """

    default_headers: Mapping[str, str] | None = None

    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        timeout: AIOHTTPTimeoutTypes = DEFAULT_AIOTTP_TIMEOUT,
        default_headers: Mapping[str, str] | None = None,
        session: Optional[aiohttp.ClientSession] = None,
    ):
        super().__init__(base_url, api_key, timeout)

        if self.api_key is None:
            raise ShuttleAIException(
                "API key not provided. Please set SHUTTLEAI_API_KEY environment variable.\n"
                + "Alternatively, you may pass it as an argument to the ShuttleAI class constructor as `api_key`.\n"
                + "In addition to that, you can also set the api key after creating the ShuttleAI object by setting \
                    `client.api_key`.\n"
            )

        self._timeout = timeout if isinstance(timeout, ClientTimeout) else ClientTimeout(total=timeout)
        if default_headers:
            self.default_headers = default_headers

        self._session: Optional[aiohttp.ClientSession] = None
        if session:
            self._session = session

        self.chat: resources.AsyncChat = resources.AsyncChat(self)
        self.images: resources.AsyncImages = resources.AsyncImages(self)
        self.audio: resources.AsyncAudio = resources.AsyncAudio(self)
        self.moderations: resources.AsyncModerations = resources.AsyncModerations(self)
        self.embeddings: resources.AsyncEmbeddings = resources.AsyncEmbeddings(self)
        self.insults: resources.AsyncInsults = resources.AsyncInsults(self)
        self.jokes: resources.AsyncJokes = resources.AsyncJokes(self)
        self.web: resources.AsyncWeb = resources.AsyncWeb(self)

    async def __aenter__(self) -> "AsyncShuttleAI":
        if self._session is None:
            self._session = aiohttp.ClientSession(timeout=self._timeout)
        return self

    async def __aexit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: Optional[Type[BaseException]],
    ) -> None:
        await self.close()

    async def close(self) -> None:
        if self._session:
            await self._session.close()
            self._session = None

    async def _check_response_status_codes(self, response: aiohttp.ClientResponse) -> None:
        if response.status in {429, 500, 502, 503, 504}:
            raise ShuttleAIAPIStatusException.from_response(
                response,
                message=f"Status: {response.status}. Message: {await response.text()}",
            )
        elif 400 <= response.status < 500:
            raise ShuttleAIAPIException.from_response(
                response,
                message=f"Status: {response.status}. Message: {await response.text()}",
            )
        elif response.status >= 500:
            raise ShuttleAIException(
                message=f"Status: {response.status}. Message: {await response.text()}",
            )

    async def _check_response(self, response: aiohttp.ClientResponse) -> Dict[str, Any]:
        await self._check_response_status_codes(response)

        json_response: Dict[str, Any] = orjson.loads(await response.read())

        return json_response

    async def _request(
        self,
        method: str,
        json: Optional[Dict[str, Any]],
        path: str,
        stream: bool = False,
    ) -> AsyncIterator[Dict[str, Any]]:
        if self._session is None:
            self._session = aiohttp.ClientSession(timeout=self._timeout)

        json_bytes: Any | None = None
        if json and len(json) > 0:
            if "file" in json:
                async with aopen(json["file"], "rb") as f:
                    json_bytes = {"file": await f.read()}
            else:
                json_bytes = orjson.dumps(json)

        # json_bytes: bytes | None = (
        #     orjson.dumps(json) if json and len(json) > 0 else None
        # )  # x-sai [dict to bytes]

        accept_header = "text/event-stream" if stream else "application/json"
        headers = {
            "Accept": accept_header,
            "User-Agent": f"shuttleai-python/a-{self._version}",
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

        if self.default_headers:
            headers.update(self.default_headers)

        url = f"{self._base_url}{path}"

        self._logger.debug(f"Sending request: {method} {url} {json}")

        try:
            async with self._session.request(
                method,
                url,
                headers=headers,
                data=json_bytes,
            ) as response:
                if stream:
                    async for line in response.content:
                        json_streamed_response = self._process_line(line)
                        if json_streamed_response:
                            yield json_streamed_response
                else:
                    yield await self._check_response(response)

        except aiohttp.ClientConnectorError as e:
            raise ShuttleAIConnectionException(str(e)) from e
        except aiohttp.ClientError as e:
            raise ShuttleAIException(f"Unexpected exception ({e.__class__.__name__}): {e}") from e
        except orjson.JSONDecodeError as e:
            raise ShuttleAIAPIException.from_response(
                response,
                message=f"Failed to decode json body: {await response.text()}",
            ) from e
        except ShuttleAIAPIStatusException as e:
            raise ShuttleAIAPIStatusException.from_response(response, message=str(e)) from e

    async def fetch_model(self, model_id: str) -> BaseModelCard:
        """Fetches a model by its ID

        Args:
            model_id (str): The ID of the model to fetch

        Returns:
            BaseModelCard, None]: The model if it exists
        """
        singleton_response = self._request("get", {}, f"/models/{model_id}")
        try:
            return BaseModelCard(**(await singleton_response.__anext__())["data"])
        except (pydantic_core.ValidationError, StopAsyncIteration) as e:
            raise ShuttleAIException("No response received") from e

    async def list_models(self) -> Union[ListModelsResponse, ListVerboseModelsResponse]:
        """Returns a list of the available models

        Returns:
            ListModelsResponse: A response object containing the list of models.
        """
        return await self._fetch_and_process_models("/models", ListModelsResponse)

    async def list_models_verbose(
        self,
    ) -> Union[ListVerboseModelsResponse, ListModelsResponse]:
        """Returns a list of the available models with verbose information

        Returns:
            ListVerboseModelsResponse: A response object containing the list of models.
        """
        return await self._fetch_and_process_models("/models/verbose", ListVerboseModelsResponse)

    async def _fetch_and_process_models(
        self,
        endpoint: str,
        response_class: Type[Union[ListModelsResponse, ListVerboseModelsResponse]],
    ) -> Union[ListModelsResponse, ListVerboseModelsResponse]:
        singleton_response = self._request("get", {}, endpoint)
        try:
            list_models_response = response_class(**(await singleton_response.__anext__()))
        except pydantic_core.ValidationError as e:
            raise ShuttleAIException("No response received") from e

        models_by_id = {model.id: model for model in list_models_response.data}

        for model in list_models_response.data:
            if isinstance(model, ProxyCard):
                model_parent = models_by_id.get(model.proxy_to)
                assert isinstance(model_parent, BaseModelCard)
                if model_parent:
                    model.parent = model_parent

        return list_models_response

    @overload
    async def ez_chat(
        self, text: str, model: Optional[str] = None, stream: Literal[False] = False
    ) -> ChatCompletionResponse: ...

    @overload
    async def ez_chat(
        self, text: str, model: Optional[str] = None, stream: Literal[True] = True
    ) -> AsyncIterable[ChatCompletionStreamResponse]: ...

    async def ez_chat(
        self,
        text: str,
        model: Optional[str] = None,
        stream: bool = False,
    ) -> Union[ChatCompletionResponse, AsyncIterable[ChatCompletionStreamResponse]]:
        return await self.chat.completions.create(  # type: ignore
            messages=[{"role": "user", "content": text}],
            model=model,
            stream=stream,
        )
