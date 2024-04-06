__version__ = "3.8.8"

from .client import ShuttleAsyncClient, ShuttleClient

from sys import executable
from os import system
from httpx import get


try:
    CURRENT_VERSION = get(
        "https://pypi.org/pypi/shuttleai/json").json().get("info").get("version")
except:
    CURRENT_VERSION = __version__

if __version__ < CURRENT_VERSION:
    print("[shuttleai] Version Out-of-Date. Please upgrade by using: \"python.exe -m pip install -U shuttleai\"")
    system(f"{executable} -m pip install -U shuttleai -q")

__all__ = ['ShuttleAI', 'AsyncShuttleAI']
