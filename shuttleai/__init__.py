__title__ = "shuttleai"
__version__ = "4.1.4"

from ._patch import _patch_httpx
from .client import AsyncShuttleAI, ShuttleAI

_patch_httpx()

__all__ = ["ShuttleAI", "AsyncShuttleAI"]
