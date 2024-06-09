__title__ = "shuttleai"
__version__ = "4.1.7"


import json
import time
import typing
from pathlib import Path

import requests
from packaging import version

from ._patch import _patch_httpx
from .client import AsyncShuttleAI, ShuttleAI

CACHE_FILE = Path(f"{__title__}-version.json")
CACHE_DURATION = 86400  # 24 hours in seconds

def read_cached_version_info() -> dict[str, typing.Any] | None:
    if CACHE_FILE.exists():
        try:
            with open(CACHE_FILE, "r") as file:
                return json.load(file)  # type: ignore
        except Exception as e:
            print(f"Error reading cache file: {e}")
    return None

def write_cached_version_info(version_info: dict) -> None:
    try:
        with open(CACHE_FILE, "w") as file:
            json.dump(version_info, file)
    except Exception as e:
        print(f"Error writing to cache file: {e}")

def check_for_updates() -> None:
    cached_version_info = read_cached_version_info()

    if cached_version_info:
        cache_time = cached_version_info.get("time")
        if cache_time and time.time() - cache_time < CACHE_DURATION:
            latest_version = cached_version_info.get("version")
            if latest_version:
                if version.parse(__version__) < version.parse(latest_version):
                    print(f"WARNING: You are using an outdated version of {__title__} ({__version__}). "
                          f"The latest version is {latest_version}. It is recommended to upgrade using:\n"
                          f">> pip install -U {__title__}")
                return

    try:
        response = requests.get("https://pypi.org/pypi/shuttleai/json")
        latest_version = response.json()["info"]["version"]
        write_cached_version_info({"version": latest_version, "time": time.time()})

        if version.parse(__version__) < version.parse(latest_version):
            print(f"WARNING: You are using an outdated version of {__title__} ({__version__}). "
                  f"The latest version is {latest_version}. It is recommended to upgrade using:\n"
                  f">> pip install -U {__title__}")
    except Exception as e:
        print(f"Could not check for updates: {e}")

_patch_httpx()
check_for_updates()

__all__ = ["ShuttleAI", "AsyncShuttleAI"]
