from .shuttleai import ShuttleClient
from .shuttleai_async import ShuttleAsyncClient

import os
from sys import executable
from os import system
from httpx import get

__version__ = "3.1"

try:
    CURRENT_VERSION = get(
        "https://pypi.org/pypi/shuttleai/json").json().get("info").get("version")
except:
    CURRENT_VERSION = __version__

if __version__ < CURRENT_VERSION:
    print("[shuttleai] Version Out-of-Date. Please upgrade by using: \"python.exe -m pip install -U shuttleai\"")
    system(f"{executable} -m pip install -U shuttleai -q")

api_key = os.environ.get("SHUTTLE_API_KEY")

__all__ = ['ShuttleClient', 'ShuttleAsyncClient']
