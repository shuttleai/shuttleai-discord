#!/usr/bin/env python


import asyncio

from shuttleai import AsyncShuttleAI


async def main() -> None:
    client = AsyncShuttleAI()

    list_models_response = await client.list_models()

    # Be sure to close the client session when not using context managers
    # (see examples/async_chat_context_manager.py for an example of using a context manager)
    await client.close()

    print(list_models_response)


if __name__ == "__main__":
    asyncio.run(main())
