#!/usr/bin/env python


import asyncio

from shuttleai import AsyncShuttleAI


async def main() -> None:
    client = AsyncShuttleAI()

    list_models_response = await client.list_models()

    print(list_models_response)

    # It is a good idea to close the client session when not using context managers
    # (see examples/async_chat_context_manager.py for an example of using a context manager)
    await client.close()


if __name__ == "__main__":
    asyncio.run(main())
