#!/usr/bin/env python

from shuttleai.client._sync import ShuttleAIClient
from shuttleai.schemas.chat_completion import ChatMessage


def main():
    model = "shuttle-2-turbo"

    client = ShuttleAIClient()

    response = client.chat.completions.create(
        model=model,
        messages=[ChatMessage(role="user", content="What is the best French cheese?")],
        stream=True
    )

    for chat in response:
        print(chat.choices[0].delta.content or "", end="", flush=True)


if __name__ == "__main__":
    main()
