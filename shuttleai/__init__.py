__title__ = "shuttleai"
__version__ = "4.6.0"

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


def read_cached_version_info() -> typing.Optional[dict[str, typing.Any]]:
    """Read the cached version information from the cache file."""
    if CACHE_FILE.exists():
        try:
            with open(CACHE_FILE, "r") as file:
                return json.load(file)  # type: ignore
        except (json.JSONDecodeError, IOError) as e:
            print(f"Error reading cache file: {e}")
    return None


def write_cached_version_info(version_info: dict[str, typing.Any]) -> None:
    """Write the version information to the cache file."""
    try:
        with open(CACHE_FILE, "w") as file:
            json.dump(version_info, file)
    except IOError as e:
        print(f"Error writing to cache file: {e}")


def is_cache_valid(cache_time: float) -> bool:
    """Check if the cache is still valid based on the cache duration."""
    return time.time() - cache_time < CACHE_DURATION


def check_for_updates() -> None:
    """Check for updates and notify the user if a newer version is available."""
    cached_version_info = read_cached_version_info()

    if cached_version_info:
        cache_time = cached_version_info.get("time")
        if cache_time and is_cache_valid(cache_time):
            latest_version = cached_version_info.get("version")
            if latest_version and version.parse(__version__) < version.parse(latest_version):
                print_update_message(latest_version)
            return

    try:
        response = requests.get("https://pypi.org/pypi/shuttleai/json")
        response.raise_for_status()
        latest_version = response.json()["info"]["version"]
        write_cached_version_info({"version": latest_version, "time": time.time()})
        if version.parse(__version__) < version.parse(latest_version):
            print_update_message(latest_version)
    except requests.RequestException as e:
        print(f"Could not check for updates: {e}")


def print_update_message(latest_version: str) -> None:
    """Print a message to the user indicating that an update is available."""
    print(
        f"WARNING: You are using an outdated version of {__title__} ({__version__}). "
        f"The latest version is {latest_version}. It is recommended to upgrade using:\n"
        f">> pip install -U {__title__}"
    )


_patch_httpx()
check_for_updates()


__all__ = ["ShuttleAI", "AsyncShuttleAI"]
