"""
@Author: ShuttleAI
@Version: 3.7
@Date: 4-3-2024
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
from ..schemas import (
    ShuttleError,
    Model,
    Models,
    ChatChunk,
    Chat,
    Image,
    Audio,
    Embedding
    )
from ..log import log
import aiohttp
import orjson
import os


class ShuttleAsyncClient:
    """
    The asynchronous client for interacting with the ShuttleAI API.

    - The client can be used as a context manager to automatically close the aiohttp.ClientSession.
    Example:
    ```python
    async with ShuttleAsyncClient() as client:
        models = await client.get_models()
        print(models)
    ```

    - The client can also be used without a context manager, which requires the user to manually close the aiohttp.ClientSession.
    Example:
    ```python
    client = ShuttleAsyncClient()
    models = await client.get_models()
    print(models)
    await client.close()
    ```

    (Not specifying an api_key defaults the api_key to the SHUTTLEAI_API_KEY environment variable)
    """
    _session: Optional[aiohttp.ClientSession] = None

    def __init__(
            self,
            api_key: Optional[str] = None,
            base_url: Optional[str] = None,
            timeout: Union[float, aiohttp.ClientTimeout, None] = 60.0,
            session: Optional[aiohttp.ClientSession] = None,
            silent: bool = True
    ):
        """
        Initialize the ShuttleAsyncClient client.

        Args:
            api_key (Optional[str], optional): The API key. Defaults to SHUTTLEAI_API_KEY environment variable.
            base_url (Optional[str], optional): The base URL for the API. Defaults to https://api.shuttleai.app/v1.
            timeout (Union[float, aiohttp.ClientTimeout, None], optional): The timeout for the aiohttp.ClientSession. Defaults to 60.0.
            session (Optional[aiohttp.ClientSession], optional): An existing aiohttp.ClientSession. Defaults to None.
            silent (bool, optional): Whether to silent debugging messages. Defaults to True.
        """
        self.silent = silent
        if session is not None:
            if not isinstance(session, aiohttp.ClientSession):
                raise TypeError(
                    f"session must be an instance of aiohttp.ClientSession, not {type(session)}"
                )
            if session.closed:
                raise ValueError("session is closed")
            if not silent:
                log.info("Using provided aiohttp.ClientSession")

            self._session = session
        else:
            if self._session is None:
                if isinstance(timeout, float):
                    timeout = aiohttp.ClientTimeout(total=timeout)
                elif not isinstance(timeout, aiohttp.ClientTimeout):
                    raise TypeError(
                        f"timeout must be a float or aiohttp.ClientTimeout, not {type(timeout)}"
                    )
                self._session = aiohttp.ClientSession(timeout=timeout, json_serialize=lambda x: orjson.dumps(x).decode())
            if not silent:
                log.info("registered new aiohttp.ClientSession")


        if api_key is None:
            api_key = os.environ.get("SHUTTLEAI_API_KEY")
            if api_key is not None and not silent:
                log.info("using SHUTTLEAI_API_KEY environment variable")
        if api_key is None:
            raise Exception("the api_key client option must be set either by passing api_key to the client or by setting the SHUTTLEAI_API_KEY environment variable")
        self.api_key = api_key

        if base_url is None:
            base_url = os.environ.get("SHUTTLEAI_BASE_URL")
            if base_url is not None and not silent:
                log.info("using SHUTTLEAI_BASE_URL environment variable")
        if base_url is None:
            base_url = "https://api.shuttleai.app/v1"
        self.base_url = base_url

    async def __aenter__(self):
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()
        return None
    
    async def close(self) -> None:
        if self._session is not None and self._session.closed is False:
            if not self._session.closed:
                if not self._session.connector.closed:
                    await self._session.close()
                else:
                    self._session.connector.close()
                    await self._session.close()
        if not self.silent:
            log.info("closed aiohttp.ClientSession")
        return None
    
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
                async with self._session.request(
                    method, url, json=data, headers=headers, params=args, data=files
                ) as response:
                    if response.status != 200:
                        data_to_yield = orjson.loads(await response.text())
                        yield data_to_yield
                        return

                    async for line in response.content.__aiter__():
                        try:
                            line = line.decode('utf-8')
                            yield orjson.loads(line.replace('data: ', ''))
                        except:
                            pass
            return streamer()
        else:
            async with self._session.request(
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

        Raises:
            Aiohttp.ClientError: If the API request failed.
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
    ) -> Union[Model, ShuttleError]:
        """
        Get information about a specific model.

        Args:
            model (str): The model name.

        Returns:
            Model: Model information or None if not found.

        Raises:
            ShuttleError: If the API request fails.
            Aiohttp.ClientError: If the API request is invalid.
        """
        try:
            response = await self._make_request("GET", f"models/{model}")
            try:
                return Model.model_validate(response)
            except:
                try:
                    return ShuttleError.model_validate(response)
                except:
                    return response
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
    ) -> Union[Chat, AsyncGenerator[Union[ChatChunk, ShuttleError, Dict[str, Any]], ShuttleError, None]]:
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
    ) -> Union[Image, ShuttleError]:
        """
        Generate images using a model.

        Args:
            model (str): The model name.
            prompt (str): The prompt for image generation.
            n (int, optional): Number of images to generate. Defaults to 1.

        Returns:
            Image: The generated image.

        Raises:
            ShuttleError: If the API request fails.
            Aiohttp.ClientError: If the API request is invalid.
        """
        try:
            data = {"model": model, "prompt": prompt, "n": n}
            response = await self._make_request(
                "POST", "images/generations", data, headers={"Authorization": f"Bearer {self.api_key}"}
            )
            try:
                return Image.model_validate(response)
            except:
                try:
                    return ShuttleError.model_validate(response)
                except:
                    return response
        except aiohttp.ClientError as e:
            log.error(f"Failed to generate images: {e}")
            raise

    async def audio_generations(
        self,
        input: str,
        voice: str,
        model: str = "ElevenLabs"
    ) -> Union[Audio, ShuttleError]:
        """
        Generate audio using a model.

        Args:
            input (str): The input for audio generation.
            voice (str): The desired voice for the audio.
            model (str, optional): The model name. Defaults to "ElevenLabs".

        Returns:
            Audio: The generated audio.

        Raises:
            ShuttleError: If the API request fails.
            Aiohttp.ClientError: If the API request is invalid.
        """
        try:
            data = {"model": model, "input": input, "voice": voice}
            response = await self._make_request(
                "POST", "audio/generations", data, headers={"Authorization": f"Bearer {self.api_key}"}
            )
            try:
                return Audio.model_validate(response)
            except:
                try:
                    return ShuttleError.model_validate(response)
                except:
                    return response
        except aiohttp.ClientError as e:
            log.error(f"Failed to generate audio: {e}")
            raise

    async def audio_transcriptions(
        self,
        file: str,
        model: str = "whisper-large"
    ) -> Union[Dict[str, Any], ShuttleError]:
        """
        Transcribe audio using a model.

        Args:
            file (str): Path to the audio file for transcription.
            model (str, optional): The model name. Defaults to "whisper-large".

        Returns:
            Dict[str, Any]: The transcription result.

        Raises:
            ShuttleError: If the API request fails.
            Aiohttp.ClientError: If the API request is invalid.
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
    ) -> Union[Dict[str, Any], ShuttleError]:
        """
        Moderate text using a model.

        Args:
            input (str): The text to moderate.
            model (str, optional): The model name. Defaults to 'text-moderation-007'.

        Returns:
            Dict[str, Any]: Moderation results.

        Raises:
            ShuttleError: If the API request fails.
            Aiohttp.ClientError: If the API request is invalid.
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
    ) -> Union[Embedding, ShuttleError]:
        """
        Generate embeddings using a model.

        Args:
            input (Union[str, List[str]]): The input text or list of texts.
            model (str, optional): The model name. Defaults to 'text-embedding-ada-002'.

        Returns:
            Embedding: The generated embeddings.

        Raises:
            ShuttleError: If the API request fails.
            Aiohttp.ClientError: If the API request is invalid.
        """
        try:
            input = [input] if isinstance(input, str) else input
            data = {"model": model, "input": input, "encoding_format": "float"}
            response = await self._make_request(
                "POST", "embeddings", data, headers={"Authorization": f"Bearer {self.api_key}"}
            )
            try:
                return Embedding.model_validate(response)
            except:
                try:
                    return ShuttleError.model_validate(response)
                except:
                    return response
        except aiohttp.ClientError as e:
            log.error(f"Failed to generate embeddings: {e}")
            raise