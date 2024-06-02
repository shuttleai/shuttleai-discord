import posixpath
from json import JSONDecodeError
from typing import Any, Dict, Iterator, Optional

import orjson
import pydantic_core
from httpx import Client, ConnectError, HTTPTransport, RequestError, Response

from shuttleai import resources
from shuttleai.client.base import ClientBase
from shuttleai.exceptions import (
    ShuttleAIAPIException,
    ShuttleAIAPIStatusException,
    ShuttleAIConnectionException,
    ShuttleAIException,
)
from shuttleai.schemas.models.models import BaseModelCard, ListModelsResponse, ListVerboseModelsResponse, ProxyCard


class ShuttleAIClient(ClientBase):
    """
    Synchronous wrapper for the ShuttleAI API
    """
    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: str = "https://api.shuttleai.app",
        timeout: int = 120,
        client: Optional[Client] = None,
    ):
        super().__init__(base_url, api_key, timeout)

        if client:
            self._client = client
        else:
            self._client = Client(
                follow_redirects=True, timeout=self._timeout, transport=HTTPTransport(retries=0)
            )

        self.chat: resources.Chat = resources.Chat(self, async_mode=False)
        self.images: resources.Images = resources.Images(self, async_mode=False)

    def __del__(self) -> None:
        self._client.close()

    def _check_response_status_codes(self, response: Response) -> None:
        if response.status_code in {429, 500, 502, 503, 504}:
            raise ShuttleAIAPIStatusException.from_response(
                response,
                message=f"Status: {response.status_code}. Message: {response.text}",
            )
        elif 400 <= response.status_code < 500:
            if response.stream:
                response.read()
            raise ShuttleAIAPIException.from_response(
                response,
                message=f"Status: {response.status_code}. Message: {response.text}",
            )
        elif response.status_code >= 500:
            if response.stream:
                response.read()
            raise ShuttleAIException(
                message=f"Status: {response.status_code}. Message: {response.text}",
            )

    def _check_streaming_response(self, response: Response) -> None:
        self._check_response_status_codes(response)

    def _check_response(self, response: Response) -> Dict[str, Any]:
        self._check_response_status_codes(response)

        json_response: Dict[str, Any] = orjson.loads(response.content)

        return json_response

    def _request(
        self,
        method: str,
        json: Optional[Dict[str, Any]],
        path: str,
        stream: bool = False,
    ) -> Iterator[Dict[str, Any]]:
        json: bytes | None = orjson.dumps(json) if json and len(json) > 0 else None # x-sai [dict to bytes]

        accept_header = "text/event-stream" if stream else "application/json"
        headers = {
            "Accept": accept_header,
            "User-Agent": f"shuttleai-client-python/{self._version}",
            "Authorization": f"Bearer {self._api_key}",
            "Content-Type": "application/json",
        }

        url = posixpath.join(self._base_url, path)

        self._logger.debug(f"Sending request: {method} {url} {json}")

        response: Response

        try:
            if stream:
                with self._client.stream(
                    method,
                    url,
                    headers=headers,
                    json=json,
                ) as response:
                    self._check_streaming_response(response)

                    for line in response.iter_lines():
                        json_streamed_response = self._process_line(line)
                        if json_streamed_response:
                            yield json_streamed_response

            else:
                response = self._client.request(
                    method,
                    url,
                    headers=headers,
                    json=json,
                )

                yield self._check_response(response)

        except ConnectError as e:
            raise ShuttleAIConnectionException(str(e)) from e
        except RequestError as e:
            raise ShuttleAIException(f"Unexpected exception ({e.__class__.__name__}): {e}") from e
        except JSONDecodeError as e:
            raise ShuttleAIAPIException.from_response(
                response,
                message=f"Failed to decode json body: {response.text}",
            ) from e
        except ShuttleAIAPIStatusException as e:
            raise ShuttleAIAPIStatusException.from_response(response, message=str(e)) from e

    def fetch_model(self, model_id: str) -> BaseModelCard:
        """Fetches a model by its ID

        Args:
            model_id (str): The ID of the model to fetch

        Returns:
            BaseModelCard, None]: The model if it exists
        """
        singleton_response = self._request("get", {}, f"v1/models/{model_id}")
        try:
            return BaseModelCard(**next(singleton_response)["data"])
        except (pydantic_core.ValidationError, StopIteration) as e:
            raise ShuttleAIException("No response received") from e

    def list_models(self) -> ListModelsResponse:
        """Returns a list of the available models

        Returns:
            ListModelsResponse: A response object containing the list of models.
        """
        return self._fetch_and_process_models("v1/models", ListModelsResponse)

    def list_models_verbose(self) -> ListVerboseModelsResponse:
        """Returns a list of the available models with verbose information

        Returns:
            ListVerboseModelsResponse: A response object containing the list of models.
        """
        return self._fetch_and_process_models("v1/models/verbose", ListVerboseModelsResponse)

    def _fetch_and_process_models(self, endpoint: str, response_class: Any) -> Any:
        singleton_response = self._request("get", {}, endpoint)
        try:
            list_models_response = response_class(**next(singleton_response))
        except pydantic_core.ValidationError as e:
            raise ShuttleAIException("No response received") from e

        models_by_id = {model.id: model for model in list_models_response.data}

        for model in list_models_response.data:
            if isinstance(model, ProxyCard):
                model.parent = models_by_id.get(model.proxy_to)

        return list_models_response
