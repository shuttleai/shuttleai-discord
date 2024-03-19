import asyncio, json
from shuttleai import ShuttleAsyncClient
from shuttleai.schemas import ChatChunk, Chat, ShuttleError

async def test():
    async with ShuttleAsyncClient("shuttle-invalid-key", 123) as shuttle:
        """Stream Test"""
        # response = await shuttle.chat_completion(
        #     model='shuttle-turbo',
        #     messages="write a short story about a cat and a mouse",
        #     plain=True,
        #     stream=True
        # )
        # async for chunk in response:
        #     if isinstance(chunk, ChatChunk):
        #         result = chunk.choices[0].delta.content
        #     elif isinstance(chunk, ShuttleError):
        #         result = json.dumps(chunk.model_dump(), indent=4, sort_keys=True)
        #     print(result, flush=True, sep='', end='')
        """Non-Stream Test"""
        # response = await shuttle.chat_completion(
        #     model='shuttle-turbo',
        #     messages="write a short story aboute a cat and a mouse",
        #     plain=True
        # )
        # if isinstance(response, Chat):
        #     result = response.choices[0].message.content
        # elif isinstance(response, ShuttleError):
        #     result = json.dumps(response.model_dump(), indent=4, sort_keys=True)
        # print(result)

if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    loop.run_until_complete(test())
