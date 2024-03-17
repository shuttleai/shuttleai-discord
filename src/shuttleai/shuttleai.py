"""
@Author: ShuttleAI
@Version: 3.1
@Date: 3-16-2024
"""
from typing import Any, Dict, List, Union, TYPE_CHECKING

import httpx
from .log import log
from .schemas import Chat, Image, Audio, Embedding

if TYPE_CHECKING:
    from httpx import Response


class ShuttleClient:
    """
    A synchronous client for interacting with the ShuttleAI API using Python.

    Use `ShuttleAsyncClient` for asynchronous API calls.

    Args:
        api_key (str): The ShuttleAI API key to use for authentication.
    """

    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.shuttleai.app/v1"

    @property
    def models(self) -> Dict[str, Any]:
        try:
            url = f"{self.base_url}/models"
            response = httpx.get(url, timeout=60)
            return response.json() if response.status_code == 200 else {}
        except Exception as e:
            log.error(f"[ShuttleAI] Error: {e}")

    def chat_completion(
        self,
        model: str,
        messages: Union[str, List[Dict[str, str]]],
        stream: bool = False,
        plain: bool = False,
        **kwargs: Any
    ) -> Union[Chat, str]:
        try:
            url = f"{self.base_url}/chat/completions"
            headers = {"Authorization": f"Bearer {self.api_key}"}

            if plain:
                messages = [{"role": "user", "content": messages}]

            data = {
                "model": model,
                "messages": messages,
                "stream": stream,
                **{key: value for key, value in kwargs.items() if value is not None},
            }

            response = httpx.post(url, json=data, headers=headers, timeout=60)
            return Chat.parse_obj(response.json()) if not stream else response.text # TODO: Use ChatChunk and actually yield the stream live
        except Exception as e:
            log.error(f"[ShuttleAI] Error: {e}")

    def images_generations(
        self,
        model: str,
        prompt: str,
        n: int = 1
    ) -> Image:
        try:
            url = f"{self.base_url}/images/generations"
            headers = {"Authorization": f"Bearer {self.api_key}"}
            data = {
                "model": model,
                "prompt": prompt,
                "n": n
            }
            response = httpx.post(url, json=data, headers=headers, timeout=60)
            return Image.parse_obj(response.json()) if response.status_code == 200 else {}
        except Exception as e:
            log.error(f"[ShuttleAI] Error: {e}")

    def audio_generations(
        self,
        input_str: str,
        voice: str,
        model: str = "ElevenLabs"
    ) -> Audio:
        try:
            url = f"{self.base_url}/audio/generations"
            headers = {"Authorization": f"Bearer {self.api_key}"}
            data = {
                "model": model,
                "input": input_str,
                "voice": voice
            }
            response = httpx.post(url, json=data, headers=headers, timeout=60)
            return Audio.parse_obj(response.json()) if response.status_code == 200 else {}
        except Exception as e:
            log.error(f"[ShuttleAI] Error: {e}")
