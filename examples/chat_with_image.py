#!/usr/bin/env python


from shuttleai import ShuttleAI
from shuttleai.schemas.chat.completions import (  # Helper for messages
    ChatMessage,
    ChatMessageContentPartImage,  # For v5 use
    ChatMessageContentPartText,  # For v5 use
)


def main() -> None:
    model = "shuttle-2-turbo"

    client = ShuttleAI()

    chat_response = client.chat.completions.create(
        model=model,
        messages=[
            ChatMessage(
                role="user",
                content="what is in this image?"
            )
        ],
        image="https://upload.wikimedia.org/wikipedia/commons/thumb/d/dd/Gfp-wisconsin-madison-the-nature-boardwalk.jpg/2560px-Gfp-wisconsin-madison-the-nature-boardwalk.jpg"
    )
    print(chat_response.choices[0].message.content)


if __name__ == "__main__":
    main()
