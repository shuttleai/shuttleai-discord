__title__ = "shuttleai"
__version__ = "4.0.5"

from ._patch import _patch_httpx
from .client import ShuttleAIAsyncClient, ShuttleAIClient

_patch_httpx()

__all__ = ["ShuttleAIClient", "ShuttleAIAsyncClient"]
