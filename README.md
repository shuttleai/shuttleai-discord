# The official Python library for the ShuttleAI API

```py
import asyncio
from shuttleai import *

SHUTTLE_KEY = "ShuttleAPI Key"

async def main():
    async with ShuttleAsyncClient(SHUTTLE_KEY, timeout=60) as shuttle:
        """Optionally change base url"""
        # shuttle.base_url = "https://api.shuttleai.app/v1"

        """Get Models Example"""
        # response = await shuttle.get_models()
        # print(response)
        """Get Model Example"""
        # response = await shuttle.get_model("gpt-4")
        # print(response)
        """Streaming Example"""
        # response = await shuttle.chat_completion(
        #     model="gpt-3.5-turbo",
        #     messages="write me a short story about bees",
        #     stream=True,
        #     plain=True,
        #     internet=False
        # )
        # async for chunk in response:
        #     try:
        #         print(chunk['choices'][0]['delta']['content'])
        #     except:
        #         pass
        """Non-Streaming Example"""
        # response = await shuttle.chat_completion(
        #     model="gpt-3.5-turbo",
        #     messages=[{"role":"user","content":"write me a short story about bees"}],
        #     stream=False,
        #     plain=False,
        #     internet=False,
        #     max_tokens=100,
        #     temperature=0.5,
        #     image="https://www.google.com/images/branding/googlelogo/1x/googlelogo_color_272x92dp.png"
        # )
        # print(response)
        """Image Generation Example"""
        # response = await shuttle.images_generations(
        #     model='sdxl',
        #     prompt='a cute cat',
        #     n=1,
        # )
        # print(response)
        """Audio Generation Example"""
        # response = await shuttle.audio_generations(
        #     model='eleven-labs-999',
        #     input='Once upon a time, there was a cute cat wondering through a dark, cold forest.',
        #     voice="mimi"
        # )
        # print(response)
        """Audio Transcription Example"""
        # response = await shuttle.audio_transcriptions(
        #     model='whisper-large',
        #     file="test.mp3"
        # )
        # print(response)
        """Moderation Example"""
        # response = await shuttle.moderations(
        #     model='text-moderation-007',
        #     input="I hate you"
        # )
        # print(response)
        """Embeddings Example"""
        # response = await shuttle.embeddings(
        #     model='text-embedding-ada-002',
        #     input="Hello there world"
        # )
        # print(response)


if __name__ == "__main__":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(main())
```