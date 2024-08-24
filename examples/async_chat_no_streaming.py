#!/usr/bin/env python


import asyncio

from shuttleai import AsyncShuttleAI


async def main() -> None:
    client = AsyncShuttleAI()

    chat_response = await client.chat.completions.create(
        messages=[{"role": "user", "content": "what is 5 plus 3"}],
        model="shuttle-2.5"
    )

    print(chat_response.choices[0].message.content)

    # Be sure to close the client session when not using context managers
    await client.close()


if __name__ == "__main__":
    asyncio.run(main())
