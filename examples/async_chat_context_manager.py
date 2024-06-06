#!/usr/bin/env python


import asyncio

from shuttleai import AsyncShuttleAI


async def main() -> None:
    async with AsyncShuttleAI() as client:
    # No need to manually close when using context manager
        chat_response = await client.chat.completions.create(
            messages=[{"role": "user", "content": "what is 5 plus 3"}],
            model="shuttle-2-turbo"
        )
        print(chat_response.choices[0].message.content)


if __name__ == "__main__":
    asyncio.run(main())
