from shuttleai import ShuttleAIClient
from shuttleai.schemas.chat_completion import ChatMessage  # Helper for messages


def main() -> None:
    model = "shuttle-2-turbo"

    client = ShuttleAIClient()

    client.api_key = "my-new-key"  # Support for changing API key after initialization
    client.base_url = "http://my-new-base.url" # Support for changing base URL after initialization
    """shuttleai handles the format of the base URL differently from the openai sdk.

    OpenAI SDK Format: https://api.openai.com/v1
    ShuttleAI SDK Format: https://api.shuttleai.app

    NOTE that the openai sdk requires the version number to be included in the base URL;
    the shuttleai sdk does not require this. The version number is included in the
    endpoint URL instead."""

    chat_response = client.chat.completions.create(
        model=model,
        messages=[ChatMessage(role="user", content="what is 5 plus 3")],
    )
    print(chat_response.choices[0].message.content)
    print("Object ID:", chat_response.id)
    print("Request ID:", chat_response.request_id)
    print("Provider ID:", chat_response.provider_id)


if __name__ == "__main__":
    main()
