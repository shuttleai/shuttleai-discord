from utils import SHUTTLEAI_API_KEY
from shuttleai import AsyncShuttleAI, ShuttleAI

from typing import AsyncGenerator, List, Union, Dict, Any, Literal

"""
This class will be to manage the API calls to ShuttleAI.

We will handle everything 100% asynchronously, so that we can make multiple calls at once with 0 blocking.

Knowing that ShuttleAsyncClient is an async context manager, utilizing __aenter__ and __aexit__ methods, we will need to ensure that only one session is created and used for the fastest speeds.

This one session will be used for all calls, chat and non-chat.
"""

class ShuttleAIManager:
    def __init__(self):
        self.client: AsyncShuttleAI = AsyncShuttleAI()
        self.session_opened = False

    async def _ensure_session(self):
        if not self.session_opened:
            await self.client.__aenter__()
            self.session_opened = True

    async def close(self):
        if self.session_opened:
            await self.client.__aexit__(None, None, None)
            self.session_opened = False

    async def ask(self, model: str, history: List[Dict[str, str]], system: str = None, image: str = None) -> AsyncGenerator[str, None]:
        """
        This method will be used to chat with the ShuttleAI API.
        """
        await self._ensure_session()
        
        messages = [{"content": system, "role": "system"}] if system else []
        messages += history

        if image:
            messages.append({"content": f"Describe {image}", "role": "user"})

        try:
            async for chunk in await self.client.chat_completion(model=model, messages=messages, stream=True):
                try:
                    yield chunk.choices[0].delta.content
                except:
                    pass
        except Exception as e:
            print(f"An error occurred: {e}")
            yield "There was an error processing your request."

    async def imagine(self, model: str, prompt: str, response_format: Literal["url", "raw"]) -> Union[str, bytes]:
        """
        This method will be used to generate images with the ShuttleAI API.
        """
        await self._ensure_session()
        try:
            response = await self.client.images.generations.generate(model, prompt)
            image = response.data[0].url
            if response_format == "url":
                return image
            else:
                async with self.client._session.get(image) as resp:
                    return await resp.read()
        except Exception as e:
            print(f"An error occurred: {e}")
            return "https://developers.google.com/static/maps/documentation/maps-static/images/error-image-generic.png"


shuttle_client = ShuttleAIManager()
