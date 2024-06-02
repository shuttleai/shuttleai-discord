import asyncio

from shuttleai.client._async import ShuttleAIAsyncClient


async def main():
    client = ShuttleAIAsyncClient()

    list_models_response = await client.list_models()

    # Be sure to close the client session when not using context managers
    await client.close()

    print(list_models_response)


if __name__ == "__main__":
    asyncio.run(main())
