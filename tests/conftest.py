import pytest

from shuttleai.client import ShuttleAIAsyncClient, ShuttleAIClient


@pytest.fixture()
def client() -> ShuttleAIClient:
    client = ShuttleAIClient()
    return client


@pytest.fixture()
def async_client() -> ShuttleAIAsyncClient:
    client = ShuttleAIAsyncClient(api_key="test_api_key")
    return client
