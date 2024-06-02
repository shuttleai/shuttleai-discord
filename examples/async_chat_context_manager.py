import asyncio

from shuttleai.client._async import ShuttleAIAsyncClient


async def main():
    async with ShuttleAIAsyncClient() as client:
        chat_response = await client.chat.completions.create(
            messages=[{"role": "user", "content": "what is 5 plus 3"}],
            model="shuttle-2-turbo"
        )

        print(chat_response.choices[0].message.content)


if __name__ == "__main__":
    asyncio.run(main())
