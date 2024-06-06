#!/usr/bin/env python


from shuttleai import ShuttleAI
from shuttleai.schemas.chat.completions import ChatMessage


def main() -> None:
    model = "shuttle-2-turbo"

    client = ShuttleAI()

    response = client.chat.completions.create(
        model=model,
        messages=[ChatMessage(role="user", content="What is the best French cheese?")],
        stream=True
    )

    for chat in response:
        print(chat.choices[0].delta.content or "", end="", flush=True)


if __name__ == "__main__":
    main()
