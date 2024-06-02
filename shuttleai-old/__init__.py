import importlib.metadata as metadata
import pathlib
import json
import time

import httpx

from .client import ShuttleClient, ShuttleAsyncClient

PACKAGE_NAME = "shuttleai"
CACHE_PATH = f'{PACKAGE_NAME}.json'

def get_latest_version():
    if pathlib.Path(CACHE_PATH).exists():
        with open(CACHE_PATH, 'r') as f:
            data = json.load(f)
            # Check if cache is expired (1 day)
            if data['latest_version']['timestamp'] < time.time() - 86400:
                return data['latest_version']['version']

    # Cache expired or doesn't exist, get latest version from PyPI
    url = f'https://pypi.org/pypi/{PACKAGE_NAME}/json'
    try:
        response = httpx.get(url, timeout=30)
        response.raise_for_status()
        data = response.json()
        latest_version = data['info']['version']
        with open(CACHE_PATH, 'w') as f:
            json.dump({'latest_version': {'version': latest_version, 'timestamp': time.time()}}, f)
        return latest_version
    except Exception as e:
        print(f"Failed to get latest version: {e}")
        return None

def is_outdated():
    try:
        latest_version = get_latest_version()
        installed_version = metadata.version(PACKAGE_NAME)
        print(f"Latest version: {latest_version}, Installed version: {installed_version}")
        print(f"Checking if {PACKAGE_NAME} is outdated...")
        return latest_version != installed_version
    except Exception as e:
        print(f"Failed to check if {PACKAGE_NAME} is outdated: {e}")
        return False

if is_outdated():
    print(f"Warning: You are using an outdated version of {PACKAGE_NAME}. Please upgrade to the latest version.")

__all__ = ['ShuttleClient', 'ShuttleAsyncClient']
