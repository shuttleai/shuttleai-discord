from __future__ import annotations

from typing import Any, Dict, Optional

from aiohttp import ClientResponse
from httpx import Response


class ShuttleAIException(Exception):
    """Base Exception class, returned when nothing more specific applies"""

    def __init__(self, message: Optional[str] = None) -> None:
        super(ShuttleAIException, self).__init__(message)

        self.message = message

    def __str__(self) -> str:
        msg = self.message or "<null>"
        return msg

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(message={str(self)})"


class ShuttleAIAPIException(ShuttleAIException):
    """Returned when the API responds with an error message"""

    def __init__(
        self,
        message: Optional[str] = None,
        http_status: Optional[int] = None,
        headers: Optional[Dict[str, Any]] = None,
    ) -> None:
        super().__init__(message)
        self.http_status = http_status
        self.headers = headers or {}

    @classmethod
    def from_response(cls, response: Response | ClientResponse, message: Optional[str] = None) -> ShuttleAIAPIException:
        return cls(
            message=(message or response.text if isinstance(response, Response) else response.reason),
            http_status=(response.status_code if isinstance(response, Response) else response.status),
        )

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(message={str(self)}, http_status={self.http_status})"


class ShuttleAIAPIStatusException(ShuttleAIAPIException):
    """Returned when we receive a non-200 response from the API that we should retry"""


class ShuttleAIConnectionException(ShuttleAIException):
    """Returned when the SDK can not reach the API server for any reason"""
