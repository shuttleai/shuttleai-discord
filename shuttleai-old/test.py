from shuttleai import ShuttleAsyncClient
from shuttleai.schemas import ChatChunk, Chat, ShuttleError
import orjson # [way faster than json](https://github.com/herumes/jsons-benchmark)

async def main():
    # async context manager example
    async with ShuttleAsyncClient(timeout=120.0) as shuttle: # if api_key not entered, default from SHUTTLEAI_API_KEY environment variable
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
        #         result = orjson.dumps(chunk.model_dump(), option=orjson.OPT_INDENT_2)
        #     print(result, flush=True, sep='', end='')
        """Non-Stream Test"""
        response = await shuttle.chat_completion(
            model='shuttle-turbo',
            messages="write a short story aboute a cat and a mouse",
            plain=True
        )
        if isinstance(response, Chat):
            result = response.choices[0].message.content
        elif isinstance(response, ShuttleError):
            result = orjson.dumps(response.model_dump(), option=orjson.OPT_INDENT_2)
        print(result)

    # no async context manager example
    # shuttle = ShuttleAsyncClient(api_key='shutl-123', silent=False)
    # response = await shuttle.chat_completion(model='shuttle-turbo', messages='Hello, how are you?', plain=True)
    # print(response)
    # await shuttle.close() # remember to close the session manually when not using async context manager


if __name__ == '__main__':
    import asyncio
    asyncio.run(main())