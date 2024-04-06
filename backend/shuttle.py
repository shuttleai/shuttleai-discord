from utils import SHUTTLEAI_API_KEY
from shuttleai import ShuttleAsyncClient, ShuttleClient
from shuttleai.schemas import ChatChunk, ShuttleError, Image

from typing import AsyncGenerator, List, Union, Dict, Any, Literal


"""
This class will be to manage the API calls to ShuttleAI.

We will handle everything 100% asynchronously, so that we can make multiple calls at once with 0 blocking.

Knowing that ShuttleAsyncClient is an async context manager, utilizing __aenter__ and __aexit__ methods, we will need to ensure that only one session is created and used for the fastest speeds.

This one session will be used for all calls, chat and non-chat.
"""

class ShuttleAIManager:
    def __init__(self):
        self.client: ShuttleAsyncClient = ShuttleAsyncClient()

    async def close(self):
        await self.client.close()
        
    async def ask(self, model: str, history: List[Dict[str, str]], system: str = None, image: str = None) -> AsyncGenerator[str, None]:
        """
        This method will be used to chat with the ShuttleAI API.
        """
        if system:
            messages = [{"content": system, "role": "system"}]
        else:
            messages = []

        messages = messages + history

        if image:
            messages.append({"content": f"Describe {image}", "role": "user"})


        async with self.client as client:
            try:
                async for chunk in await client.chat_completion(
                    model=model,
                    messages=messages,
                    stream=True
                ):
                    try:
                        yield chunk.choices[0].delta.content
                    except:
                        pass
            except Exception as e:
                print(f"An error occurred: {e}")
                yield "There was an error processing your request."
                pass

    async def imagine(self, model: str, prompt: str, response_format: Literal["url", "raw"]) -> str:
        """
        This method will be used to generate images with the ShuttleAI API.
        """
        async with self.client as client:
            try:
                response = await client.images_generations(model, prompt)
                if isinstance(response, Image):
                    image = response.data[0].url
                else:
                    image = "https://as2.ftcdn.net/v2/jpg/00/44/18/83/1000_F_44188314_xoXeYdEqwFYdApmbMSQGMdiMcDm9yb2l.jpg"
                if response_format == "url":
                    return image
                else:
                    async with client._session.get(image) as resp:
                        return await resp.read()
            except Exception as e:
                print(f"An error occurred: {e}")
                return "https://as2.ftcdn.net/v2/jpg/00/44/18/83/1000_F_44188314_xoXeYdEqwFYdApmbMSQGMdiMcDm9yb2l.jpg"


shuttle_client = ShuttleAIManager()