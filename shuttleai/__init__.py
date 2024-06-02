__title__ = "shuttleai"
__version__ = "4.0.0"
__author__ = "ShuttleAI"
__license__ = "MIT"
__description__ = "Python wrapper for the ShuttleAI API."
__url__ = "https://shuttleai.app"
__download_url__ = "https://pypi.org/project/shuttleai/"
__docs_url__ = "https://docs.shuttleai.app"
__homepage__ = "https://shuttleai.app"


from ._patch import _patch_httpx

_patch_httpx()


from .client import ShuttleAIAsyncClient, ShuttleAIClient
