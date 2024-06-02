import asyncio

from shuttleai.client._async import ShuttleAIAsyncClient


async def main():
    client = ShuttleAIAsyncClient()

    response = await client.chat.completions.create(
        messages=[{"role": "user", "content": "what is 5 plus 3"}],
        model="shuttle-2-turbo",
        stream=True
    )

    async for chunk in response:
        print(chunk.choices[0].delta.content or "", end="", flush=True)

    # Be sure to close the client session when not using context managers
    await client.close()


if __name__ == "__main__":
    asyncio.run(main())
