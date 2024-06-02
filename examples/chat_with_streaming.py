from shuttleai import ShuttleAIClient
from shuttleai.schemas.chat_completion import ChatCompletionStreamResponse, ChatMessage


def main():
    model = "shuttle-2-turbo"

    client = ShuttleAIClient()

    response = client.chat.completions.create(
        model=model,
        messages=[ChatMessage(role="user", content="What is the best French cheese?")],
        stream=True
    )

    for chat in response:
        chat: ChatCompletionStreamResponse # type hint for IDEs (only necessary for sync stream? # TODO: fix)
        print(chat.choices[0].delta.content or "", end="", flush=True)


if __name__ == "__main__":
    main()
