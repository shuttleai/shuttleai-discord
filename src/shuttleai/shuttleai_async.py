"""
@Author: ShuttleAI
@Version: 3.3
@Date: 3-22-2024
"""
from __future__ import annotations
from typing import (
    List,
    Dict,
    Any,
    Union,
    Optional,
    AsyncGenerator
)

from .schemas import (
    ShuttleError,
    Model,
    Models,
    ChatChunk,
    Chat,
    Image,
    Audio,
    Embedding
    )
from .log import log

import aiohttp
import json


class ShuttleAsyncClient:
    """
    Async client for interacting with the Shuttle AI API.
    """

    def __init__(self, api_key: str, timeout: int = 60):
        """
        Initialize the ShuttleAsyncClient.

        Args:
            api_key (str): The API key for authentication.
            timeout (int, optional): The timeout for API requests in seconds. Defaults to 60.
        """
        self.api_key = api_key
        self.base_url = "https://api.shuttleai.app/v1"
        self.timeout = timeout
        self.session: aiohttp.ClientSession

    async def __aenter__(self) -> ShuttleAsyncClient:
        """
        Async context manager entry.
        """
        self.session = aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=self.timeout))
        return self

    async def __aexit__(self, exc_type, exc_value, traceback) -> ShuttleAsyncClient:
        """
        Async context manager exit.
        """
        await self.session.close()

    async def _make_request(
        self,
        method: str,
        endpoint: str,
        data: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, Any]] = None,
        stream: bool = False,
        params: Optional[Dict[str, Any]] = None,
        file: Optional[str] = None,
    ) -> Union[Dict[str, Any], List[Dict[str, Any]]]:
        """
        Make an async HTTP request.

        Args:
            method (str): The HTTP method (GET, POST, etc.).
            endpoint (str): The API endpoint.
            data (Optional[Dict[str, Any]], optional): JSON data for the request body. Defaults to None.
            headers (Optional[Dict[str, Any]], optional): Additional headers. Defaults to None.
            stream (bool, optional): Whether the response should be streamed. Defaults to False.
            params (Optional[Dict[str, Any]], optional): URL parameters. Defaults to None.
            file (Optional[str], optional): File path for uploading. Defaults to None.

        Returns:
            Union[Dict[str, Any], List[Dict[str, Any]]]: The response data.
        """
        url = f"{self.base_url}/{endpoint}"
        args = "&".join(f"{key}={value}" for key,
                        value in params.items()) if params else ""
        files = {"file": (file, open(file, "rb"))} if file else None

        if stream:
            async def streamer():
                async with self.session.request(
                    method, url, json=data, headers=headers, params=args, data=files
                ) as response:
                    if response.status != 200:
                        data_to_yield = json.loads(await response.text())
                        yield data_to_yield
                        return

                    async for line in response.content.__aiter__():
                        try:
                            line = line.decode('utf-8')
                            yield json.loads(line.replace('data: ', ''))
                        except:
                            pass
            return streamer()
        else:
            async with self.session.request(
                method, url, json=data, headers=headers, params=args, data=files
            ) as response:
                return await response.json()

    async def get_models(
        self,
        free: bool = False,
        premium: bool = False,
        endpoint: str = "all"
    ) -> Models:
        """
        Get information about available models.

        Args:
            free (bool, optional): Whether to include free models. Defaults to False.
            premium (bool, optional): Whether to include premium models. Defaults to False.
            endpoint (str, optional): The specific model endpoint. Defaults to "all".

        Returns:
            Models: Model information.
        """
        try:
            params = {"endpoints": endpoint,
                      **({"format": "free"} if free else {"format": "premium"} if premium else {})}
            return Models.model_validate(await self._make_request("GET", "models", params=params))
        except aiohttp.ClientError as e:
            log.error(f"Failed to retrieve models: {e}")
            raise

    async def get_model(
        self,
        model: str
    ) -> Model | None:
        """
        Get information about a specific model.

        Args:
            model (str): The model name.

        Returns:
            Model: Model information or None if not found.
        """
        try:
            return Model.model_validate(await self._make_request("GET", f"models/{model}"))
        except aiohttp.ClientError as e:
            log.error(f"Failed to retrieve model information: {e}")
            return None

    async def chat_completion(
        self,
        model: str,
        messages: Union[str, List[Dict[str, Any]]],
        stream: bool = False,
        plain: bool = False,
        **kwargs
    ) -> Union[Chat, AsyncGenerator[Union[ChatChunk, ShuttleError, Dict[str, Any]], None]]:
        """
        Get chat completions from a model.

        Args:
            model (str): The model name.
            messages (Union[str, List[Dict[str, Any]]]): User messages.
            stream (bool, optional): Whether to stream the response. Defaults to False.
            plain (bool, optional): Whether messages are plain text. Defaults to False.
            **kwargs: Additional keyword arguments.

        Returns:
            Union[Chat, AsyncGenerator[Union[ChatChunk, ShuttleError, Dict[str, Any]], None]]: The completed chat or streamed response.

        Raises:
            ShuttleError: If the API request fails.
            Aiohttp.ClientError: If the API request is invalid.
        """
        try:
            messages = [{"role": "user", "content": messages}
                        ] if plain else messages
            data = {"model": model, "messages": messages,
                    "stream": stream, **kwargs}
            response = await self._make_request(
                "POST", "chat/completions", data, headers={"Authorization": f"Bearer {self.api_key}"}, stream=stream
            )
            if stream:
                async def streamer():
                    async for chunk in response:
                        try:
                            yield ChatChunk.model_validate(chunk)
                        except:
                            try:
                                yield ShuttleError.model_validate(chunk)
                            except:
                                try:
                                    yield chunk
                                except:
                                    pass
                return streamer()
            else:
                try:
                    return Chat.model_validate(response)
                except:
                    try:
                        return ShuttleError.model_validate(response)
                    except:
                        return response

        except aiohttp.ClientError as e:
            log.error(f"Failed to get chat completions: {e}")
            raise

    async def images_generations(
        self,
        model: str,
        prompt: str,
        n: int = 1
    ) -> Image:
        """
        Generate images using a model.

        Args:
            model (str): The model name.
            prompt (str): The prompt for image generation.
            n (int, optional): Number of images to generate. Defaults to 1.

        Returns:
            Image: The generated image.
        """
        try:
            data = {"model": model, "prompt": prompt, "n": n}
            return Image.model_validate(await self._make_request(
                "POST", "images/generations", data, headers={"Authorization": f"Bearer {self.api_key}"}
            ))
        except aiohttp.ClientError as e:
            log.error(f"Failed to generate images: {e}")
            raise

    async def audio_generations(
        self,
        input: str,
        voice: str,
        model: str = "ElevenLabs"
    ) -> Audio:
        """
        Generate audio using a model.

        Args:
            input (str): The input for audio generation.
            voice (str): The desired voice for the audio.
            model (str, optional): The model name. Defaults to "ElevenLabs".

        Returns:
            Audio: The generated audio.
        """
        try:
            data = {"model": model, "input": input, "voice": voice}
            return Audio.model_validate(await self._make_request(
                "POST", "audio/generations", data, headers={"Authorization": f"Bearer {self.api_key}"}
            ))
        except aiohttp.ClientError as e:
            log.error(f"Failed to generate audio: {e}")
            raise

    async def audio_transcriptions(
        self,
        file: str,
        model: str = "whisper-large"
    ) -> Dict[str, Any]:
        """
        Transcribe audio using a model.

        Args:
            file (str): Path to the audio file for transcription.
            model (str, optional): The model name. Defaults to "whisper-large".

        Returns:
            Dict[str, Any]: The transcription result.
        """
        try:
            data = {"model": model}
            return await self._make_request(
                "POST", "audio/transcriptions", data, headers={"Authorization": f"Bearer {self.api_key}"}, file=file
            )
        except aiohttp.ClientError as e:
            log.error(f"Failed to transcribe audio: {e}")
            raise

    async def moderations(
        self,
        input: str,
        model: str = 'text-moderation-latest'
    ) -> Dict[str, Any]:
        """
        Moderate text using a model.

        Args:
            input (str): The text to moderate.
            model (str, optional): The model name. Defaults to 'text-moderation-007'.

        Returns:
            Dict[str, Any]: Moderation results.
        """
        try:
            data = {"model": model, "input": input}
            return await self._make_request("POST", "moderations", data, headers={"Authorization": f"Bearer {self.api_key}"})
        except aiohttp.ClientError as e:
            log.error(f"Failed to moderate input: {e}")
            raise

    async def embeddings(
        self,
        input: Union[str, List[str]],
        model: str = 'text-embedding-ada-002'
    ) -> Embedding:
        """
        Generate embeddings using a model.

        Args:
            input (Union[str, List[str]]): The input text or list of texts.
            model (str, optional): The model name. Defaults to 'text-embedding-ada-002'.

        Returns:
            Embedding: The generated embeddings.
        """
        try:
            input = [input] if isinstance(input, str) else input
            data = {"model": model, "input": input, "encoding_format": "float"}
            return Embedding.model_validate(await self._make_request(
                "POST", "embeddings", data, headers={"Authorization": f"Bearer {self.api_key}"}
            ))
        except aiohttp.ClientError as e:
            log.error(f"Failed to generate embeddings: {e}")
            raise
