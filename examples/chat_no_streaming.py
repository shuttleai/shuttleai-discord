#!/usr/bin/env python


from shuttleai import ShuttleAIClient
from shuttleai.schemas.chat.completions import ChatMessage  # Helper for messages


def main() -> None:
    model = "shuttle-2-turbo"

    client = ShuttleAIClient()

    chat_response = client.chat.completions.create(
        model=model,
        messages=[ChatMessage(role="user", content="what is 5 plus 3")],
    )
    print(chat_response.choices[0].message.content)


if __name__ == "__main__":
    main()
