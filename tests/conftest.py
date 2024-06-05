# NOTE TESTS USES YOUR QUOTA IF API KEY IS SET
# NOTE TESTS WILL FAIL IF API KEY IS NOT SET
import pytest

from shuttleai.client import AsyncShuttleAI, ShuttleAI


@pytest.fixture()
def client() -> ShuttleAI:
    client = ShuttleAI()
    return client


@pytest.fixture()
def async_client() -> AsyncShuttleAI:
    client = AsyncShuttleAI(api_key="test_api_key")
    return client
