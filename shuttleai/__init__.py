from ._patch import _patch_httpx
from .client import ShuttleAIAsyncClient, ShuttleAIClient

_patch_httpx()

__title__ = "shuttleai"
__version__ = "4.0.4"

__all__ = ["ShuttleAIClient", "ShuttleAIAsyncClient"]
