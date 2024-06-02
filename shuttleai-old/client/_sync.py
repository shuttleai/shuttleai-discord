"""
@Author: ShuttleAI
@Date: 5-17-2024
"""
from typing import Any, Dict, List, Union, Optional, TYPE_CHECKING, Generator
if TYPE_CHECKING:
    from httpx import Response

from ..log import log
from ..schemas import Chat, ChatChunk, Image, Audio, Embedding, Models, ShuttleError, Model

import orjson
import httpx
import os


class ShuttleClient:
    """
    The synchronous client for interacting with the ShuttleAI API.
    """
    _httpx_client: Optional[httpx.Client] = None

    def __init__(
            self,
            api_key: Optional[str] = None,
            base_url: Optional[str] = None,
            timeout: Union[httpx.Timeout, float, int, None] = 60.0,
            httpx_client: Optional[httpx.Client] = None,
            silent: bool = True
    ):
        """
        Initialize the ShuttleClient.

        Args:
            api_key (Optional[str], optional): The API key. Defaults to SHUTTLEAI_API_KEY environment variable.
            base_url (Optional[str], optional): The base URL for the API. Defaults to https://api.shuttleai.app/v1.
            timeout (Union[float, aiohttp.ClientTimeout, None], optional): The timeout for the httpx.Timeout. Defaults to 60.0.
            httpx_client (Optional[httpx.Client], optional): An existing httpx.Client. Defaults to None.
            silent (bool, optional): Whether to silent debugging messages. Defaults to True.
        """
        self.silent = silent
        if httpx_client is not None:
            if not isinstance(httpx_client, httpx.Client):
                raise TypeError(
                    f"httpx_client must be an instance of httpx.Client, not {type(httpx_client)}"
                )
            if httpx_client.is_closed:
                raise ValueError("httpx_client is closed")
            if not silent:
                log.info("Using provided httpx.Client")

            self._httpx_client = httpx_client
        else:
            if self._httpx_client is None:
                if isinstance(timeout, float):
                    timeout = httpx.Timeout(timeout)
                elif isinstance(timeout, int):
                    timeout = httpx.Timeout(float(timeout))
                elif not isinstance(timeout, httpx.Timeout):
                    raise TypeError(
                        f"timeout must be a float or aiohttp.ClientTimeout, not {type(timeout)}"
                    )
                self._httpx_client = httpx.Client(timeout=timeout)
            if not silent:
                log.info("registered new httpx.Client")

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


    def __del__(self):
        self.close()

    def close(self):
        if self._httpx_client is not None and not self._httpx_client.is_closed:
            self._httpx_client.close()

    def _make_request(
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
        Make a sync HTTP request.

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
        headers = headers or {}
        headers["Authorization"] = f"Bearer {self.api_key}"
        if isinstance(data, dict):
            headers["Content-Type"] = "application/json"
        args = "&".join(f"{key}={value}" for key,
                        value in params.items()) if params else ""
        files = {"file": (file, open(file, "rb"))} if file else None

        if stream:
            def streamer():
                with self._httpx_client.stream(
                    method, url, content=orjson.dumps(data) if isinstance(data, dict) else data, headers=headers
                ) as response:
                    if response.status_code != 200:
                        try:
                            yield orjson.loads(response.text)
                        except orjson.JSONDecodeError:
                            yield response.text
                        return
                    
                    for line in response.iter_bytes():
                        try:
                            line = line.decode('utf-8')
                            yield orjson.loads(line.replace('data: ', ''))
                        except:
                            pass
            return streamer()
        else:
            response = self._httpx_client.request(
                method, url, content=orjson.dumps(data) if isinstance(data, dict) else data, headers=headers, data=files, params=args
            )
            try:
                return response.json()
            except:
                return response.text

    @property  
    def models(
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
            httpx.HTTPError: If the API request failed.
        """
        try:
            params = {"endpoints": endpoint,
                      **({"format": "free"} if free else {"format": "premium"} if premium else {})}
            return Models.from_dict(self._make_request("GET", "models", params=params))
        except httpx.HTTPError as e:
            log.error(f"Failed to retrieve models: {e}")
            raise

    def chat_completion(
        self,
        model: str,
        messages: Union[str, List[Dict[str, Any]]],
        stream: bool = False,
        plain: bool = False,
        **kwargs
    ) -> Union[Chat, Generator[Union[ChatChunk, ShuttleError, Dict[str, Any]], ShuttleError, None]]:
        """
        Get chat completions from a model.

        Args:
            model (str): The model name.
            messages (Union[str, List[Dict[str, Any]]]): User messages.
            stream (bool, optional): Whether to stream the response. Defaults to False.
            plain (bool, optional): Whether messages are plain text. Defaults to False.
            **kwargs: Additional keyword arguments.

        Returns:
            Union[Chat, Generator[Union[ChatChunk, ShuttleError, Dict[str, Any]], None]]: The completed chat or streamed response.

        Raises:
            ShuttleError: If the API request fails.
            httpx.HTTPError: If the API request is invalid.
        """
        try:
            messages = [{"role": "user", "content": messages}
                        ] if plain else messages
            data = {"model": model, "messages": messages,
                    "stream": stream, **kwargs}
            response = self._make_request(
                "POST", "chat/completions", data, stream=stream
            )
            if stream:
                def streamer():
                    for chunk in response:
                        try:
                            yield ChatChunk.from_dict(chunk)
                        except Exception as e:
                            print(e)
                            try:
                                yield ShuttleError(**chunk)
                            except:
                                try:
                                    yield chunk
                                except:
                                    pass
                return streamer()
            else:
                try:
                    return Chat.from_dict(response)
                except:
                    try:
                        return ShuttleError(**response)
                    except:
                        return response

        except httpx.HTTPError as e:
            log.error(f"Failed to get chat completions: {e}")
            raise

    def images_generations(
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
            httpx.HTTPError: If the API request is invalid.
        """
        try:
            data = {"model": model, "prompt": prompt, "n": n}
            response = self._make_request(
                "POST", "images/generations", data, headers={"Authorization": f"Bearer {self.api_key}"}
            )
            try:
                return Image.from_dict(response)
            except:
                try:
                    return ShuttleError(**response)
                except:
                    return response
        except httpx.HTTPError as e:
            log.error(f"Failed to generate images: {e}")
            raise

    def audio_generations(
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
            httpx.HTTPError: If the API request is invalid.
        """
        try:
            data = {"model": model, "input": input, "voice": voice}
            response = self._make_request(
                "POST", "audio/speech", data, headers={"Authorization": f"Bearer {self.api_key}"}
            )
            try:
                return Audio.from_dict(response)
            except:
                try:
                    return ShuttleError(**response)
                except:
                    return response
        except httpx.HTTPError as e:
            log.error(f"Failed to generate audio: {e}")
            raise

    def audio_transcriptions(
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
            httpx.HTTPError: If the API request is invalid.
        """
        try:
            data = {"model": model}
            return self._make_request(
                "POST", "audio/transcriptions", data, headers={"Authorization": f"Bearer {self.api_key}"}, file=file
            )
        except httpx.HTTPError as e:
            log.error(f"Failed to transcribe audio: {e}")
            raise

    def moderations(
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
            httpx.HTTPError: If the API request is invalid.
        """
        try:
            data = {"model": model, "input": input}
            return self._make_request("POST", "moderations", data, headers={"Authorization": f"Bearer {self.api_key}"})
        except httpx.HTTPError as e:
            log.error(f"Failed to moderate input: {e}")
            raise

    def embeddings(
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
            httpx.HTTPError: If the API request is invalid.
        """
        try:
            input = [input] if isinstance(input, str) else input
            data = {"model": model, "input": input, "encoding_format": "float"}
            response = self._make_request(
                "POST", "embeddings", data, headers={"Authorization": f"Bearer {self.api_key}"}
            )
            try:
                return Embedding(**response)
            except:
                try:
                    return ShuttleError(**response)
                except:
                    return response
        except httpx.HTTPError as e:
            log.error(f"Failed to generate embeddings: {e}")
            raise