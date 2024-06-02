#!/usr/bin/env python

from shuttleai.client._sync import ShuttleAIClient
from shuttleai.schemas.chat_completion import ChatMessage


def main():
    model = "shuttle-2-turbo"

    client = ShuttleAIClient()

    chat_response = client.chat.completions.create(
        model=model,
        messages=[ChatMessage(role="user", content="What is the best French cheese?")],
    )
    print(chat_response.choices[0].message.content)


if __name__ == "__main__":
    main()
