import pytest

from shuttleai.client import ShuttleAIAsyncClient, ShuttleAIClient


@pytest.fixture()
def client():
    client = ShuttleAIClient()
    return client


@pytest.fixture()
def async_client():
    client = ShuttleAIAsyncClient(api_key="test_api_key")
    return client
