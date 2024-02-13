"""
@Author: ShuttleAI
@Version: 2
@Date: 2-7-2024
"""

import httpx
from .log import log
import json

# class Message:
#     def __init__(self, content):
#         self.content = content

#     def to_dict(self):
#         return {'content': self.content}

# class Choice:
#     def __init__(self, message):
#         self.message = message

#     def to_dict(self):
#         return {'message': self.message.to_dict()}

# class Data:
#     def __init__(self, choices):
#         self.choices = choices

#     def to_dict(self):
#         return {'choices': [choice.to_dict() for choice in self.choices]}

# class ShuttleAIResponse:
#     def __init__(self, status_code, data):
#         self.status_code = status_code
#         self.data = Data([Choice(Message(item['message']['content'])) for item in data.get('choices', [])])

#     def __str__(self):
#         return f"ShuttleAIResponse(status_code={self.status_code}, data={self.data})"

#     def __repr__(self):
#         return self.__str__()

#     def to_json(self):
#         return json.dumps(self.data.to_dict())

# test_response = ShuttleAIResponse(200, {'choices': [{'message': {'content': "Hello World"}}]})
# print(test_response)
# print(test_response.data.choices[0].message.content)
# print(test_response.to_json())

# class ShuttleAIChunk:
#     def __init__(self, id, choices):
#         self.id = id
#         self.choices = choices

#     def __str__(self):
#         return f"ShuttleAIChunk(id={self.id}, choices={self.choices})"

#     def __repr__(self):
#         return self.__str__()

class ShuttleAsyncClient:
    """
    Asynchronous client for interacting with the Shuttle AI API.
    """

    def __init__(self, api_key, timeout=60):
        """
        Initialize the ShuttleAsyncClient.

        Args:
            api_key (str): The API key for accessing the Shuttle AI API.
            timeout (int, optional): The timeout for the HTTP request in seconds. Defaults to 60.
        """
        self.api_key = api_key 
        self.base_url = "https://api.shuttleai.app/v1"
        self.client = httpx.AsyncClient(timeout=timeout)

    async def __aenter__(self):
        """
        Enter the asynchronous context manager.
        """
        return self

    async def __aexit__(self, exc_type, exc_value, traceback):
        """
        Exit the asynchronous context manager.
        """
        await self.client.aclose()

    async def _make_request(self, method, endpoint, data=None, headers=None, stream=False, params=None, file=None):
        """
        Make an asynchronous HTTP request.

        Args:
            method (str): The HTTP method (GET, POST, etc.).
            endpoint (str): The API endpoint to send the request to.
            data (dict, optional): The data to be sent with the request (JSON format).
            headers (dict, optional): Additional headers to be included in the request.
            stream (bool, optional): Whether to stream the response.
            params (str, optional): The query parameters to be included in the request.
            file (str, optional): The file to be included in the request.

        Returns:
            dict: The JSON response from the API.

        Raises:
            Exception: If an error occurs during the request.
        """
        url = f"{self.base_url}/{endpoint}"
        if params:
            url += f"?{params}"
        if file:
            files = {"file": (file, open(file, "rb"))}
        if not stream:
            response = await self.client.request(method, url, json=data, headers=headers, files=files if file else None)
            response.raise_for_status()
            return response.json()
        else:
            async def streamer():
                async with self.client.stream(method, url, json=data, headers=headers) as response:
                    # async for chunk in response.aiter_bytes():
                    #     yield chunk
                    async for line in response.aiter_lines():
                        try:
                            yield json.loads(line.replace('data: ', ''))
                        except:
                            pass
            return streamer()

    async def get_models(self, free_only=False, premium_only=False, endpoint="all"):
        """
        Retrieve available models from the Shuttle AI API.

        Args:
            free_only (bool, optional): Whether to retrieve only free models.
            premium_only (bool, optional): Whether to retrieve only premium models.
            endpoint (str, optional): The endpoint to retrieve models for.

        Returns:
            dict: The JSON response containing available models.

        Raises:
            Exception: If an error occurs during the request.
        """
        try:
            params = []

            if endpoint != "all":
                params.append(f"endpoints={endpoint}")
            if free_only:
                params.append("format=free")
            if premium_only:
                params.append("format=premium")

            param_string = "&".join(params) if params else None

            return await self._make_request("GET", "models", params=param_string)
        except httpx.HTTPError as e:
            log.error(f"Failed to retrieve models: {e}")

    async def get_model(self, model: str):
        """
        Retrieve information about a specific model.

        Args:
            model (str): The model to retrieve information for.

        Returns:
            dict: The JSON response containing model information.

        Raises:
            Exception: If an error occurs during the request.
        """
        try:
            return await self._make_request("GET", f"models/{model}")
        except httpx.HTTPError as e:
            log.error(f"Failed to retrieve model information: {e}")
            return None
        except Exception as e:
            log.error(f"Error: {e}")
            return None

    async def chat_completion(self, model, messages, stream=False, plain=False, **kwargs):
        """
        Get chat completions from the specified model.

        Args:
            model (str): The model to use for chat completions.
            messages (list): List of messages in the conversation.
            stream (bool, optional): Whether to stream responses.
            plain (bool, optional): Whether messages are plain text.

        Kwargs: # Note: some kwargs may be limited to certain models
            max_tokens (int, optional): Maximum number of tokens to generate.
            temperature (float, optional): Temperature for sampling.
            top_p (float, optional): Top-p sampling.

            internet (bool, optional): Whether to use internet.
            citations (bool, optional): Whether to include citations.
            raw (bool, optional): Whether to return raw completion.
            image (str, optional): Image URL or base64 encoded bytes associated with the image.

        Returns:
            dict: The JSON response containing chat completions.

        Raises:
            Exception: If an error occurs during the request.
        """
        try:
            if plain:
                messages = [{"role": "user", "content": messages}]

            data = {
                "model": model,
                "messages": messages,
                "stream": stream,
            }

            for key, value in kwargs.items():
                data[key] = value if value is not None else data[key]  # Set default value if None

            return await self._make_request("POST", "chat/completions", data, headers={"Authorization": f"Bearer {self.api_key}"}, stream=stream)
        except httpx.HTTPError as e:
            log.error(f"Failed to get chat completions: {e}")

    async def images_generations(self, model, prompt, n=1):
        """
        Generate images using the specified model.

        Args:
            model (str): The model to use for image generation.
            prompt (str): The prompt for image generation.
            n (int, optional): The number of images to generate.

        Returns:
            dict: The JSON response containing generated images.

        Raises:
            Exception: If an error occurs during the request.
        """
        try:
            data = {
                "model": model,
                "prompt": prompt,
                "n": n
            }
            return await self._make_request("POST", "images/generations", data, headers={"Authorization": f"Bearer {self.api_key}"})
        except httpx.HTTPError as e:
            log.error(f"Failed to generate images: {e}")

    async def audio_generations(self, input, voice, model="ElevenLabs"):
        """
        Generate audio using the specified model.

        Args:
            input (str): The input for audio generation.
            voice (str): The voice for audio generation.
            model (str, optional): The model to use for audio generation.

        Returns:
            dict: The JSON response containing generated audio.

        Raises:
            Exception: If an error occurs during the request.
        """
        try:
            data = {
                "model": model,
                "input": input,
                "voice": voice
            }
            return await self._make_request("POST", "audio/generations", data, headers={"Authorization": f"Bearer {self.api_key}"})
        except httpx.HTTPError as e:
            log.error(f"Failed to generate audio: {e}")
    
    async def audio_transcriptions(self, file, model="whisper-large"):
        """
        Transcribe audio using the specified model.

        Args:
            file (str): The file to transcribe.
            model (str, optional): The model to use for audio transcription.

        Returns:
            dict: The JSON response containing transcribed audio.

        Raises:
            Exception: If an error occurs during the request.
        """
        try:
            data = {
                "model": model,
            }
            return await self._make_request("POST", "audio/transcriptions", data, headers={"Authorization": f"Bearer {self.api_key}"}, file=file)
        except httpx.HTTPError as e:
            log.error(f"Failed to transcribe audio: {e}")

    async def moderations(self, input, model='text-moderation-007'):
        """
        Moderate input using the specified model.

        Args:
            input (str): The input to moderate.
            model (str, optional): The model to use for moderation.

        Returns:
            dict: The JSON response containing moderated input.

        Raises:
            Exception: If an error occurs during the request.
        """
        try:
            data = {
                "model": model,
                "input": input
            }
            return await self._make_request("POST", "moderations", data, headers={"Authorization": f"Bearer {self.api_key}"})
        except httpx.HTTPError as e:
            log.error(f"Failed to moderate input: {e}")

    async def embeddings(self, input, model='text-embedding-ada-002'):
        """
        Generate embeddings for input using the specified model.

        Args:
            input (str or list): The input to generate embeddings for.
            model (str, optional): The model to use for embedding generation.

        Returns:
            dict: The JSON response containing generated embeddings.

        Raises:
            Exception: If an error occurs during the request.
        """
        try:
            if isinstance(input, str):
                input = [input]
            data = {
                "model": model,
                "input": input,
                "encoding_format": "float"
            }
            return await self._make_request("POST", "embeddings", data, headers={"Authorization": f"Bearer {self.api_key}"})
        except httpx.HTTPError as e:
            log.error(f"Failed to generate embeddings: {e}")
