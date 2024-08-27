#!/usr/bin/env python


from shuttleai import ShuttleAI
from shuttleai.exceptions import ShuttleAIAPIException
from shuttleai.schemas.chat.completions import ChatMessage  # Helper for messages, not needed!


def main() -> None:
    model = "shuttle-2.5"

    client = ShuttleAI()

    # client.api_key = "my-new-key"  # Support for changing API key after initialization
    # client.base_url = "http://my-new-base.url" # Support for changing base URL after initialization
    """shuttleai handles the format of the base URL differently from the openai sdk.

    OpenAI SDK Format: https://api.shuttleai.app/v1
    ShuttleAI SDK Format: https://api.shuttleai.app

    NOTE that the openai sdk requires the version number to be included in the base URL;
    the shuttleai sdk does not require this."""
    try:
        chat_response = client.chat.completions.create(
            model=model,
            messages=[ChatMessage(role="user", content="what is 5 plus 3")],
        )
        print(chat_response.choices[0].message.content)
        print(f"${chat_response.usage.total_charged}")
    except ShuttleAIAPIException as e:
        print(str(e))
        print(e.headers)  # can find request ID here


if __name__ == "__main__":
    main()
