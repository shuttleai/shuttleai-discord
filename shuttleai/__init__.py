__title__ = "shuttleai"
__version__ = "4.0.0"


from ._patch import _patch_httpx

_patch_httpx()


from .client import ShuttleAIAsyncClient, ShuttleAIClient
