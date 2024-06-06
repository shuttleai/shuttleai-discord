from typing import Final, Union

from aiohttp import ClientTimeout
from httpx import Timeout

DEFAULT_TIMEOUT: Final[float] = 2 * 60
DEFAULT_AIOTTP_TIMEOUT: Final[ClientTimeout] = ClientTimeout(total=DEFAULT_TIMEOUT)
DEFAULT_HTTPX_TIMEOUT: Final[Timeout] = Timeout(DEFAULT_TIMEOUT)

HTTPXTimeoutTypes = Union[
    float,
    "Timeout",
]

AIOHTTPTimeoutTypes = Union[float, "ClientTimeout"]

TimeoutTypes = Union[HTTPXTimeoutTypes, AIOHTTPTimeoutTypes]
