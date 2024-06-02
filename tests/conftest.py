from unittest import mock

import pytest
from shuttleai.client._sync import ShuttleAIClient


@pytest.fixture()
def client():
    client = ShuttleAIClient(api_key="test_api_key")
    return client