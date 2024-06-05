#!/usr/bin/env python


from shuttleai import ShuttleAIClient


def main() -> None:
    client = ShuttleAIClient()

    # Example of using ez_chat to interact with the chat completions endpoint
    # [!] Async uses same example but using await
    response = client.ez_chat(
        # Default model is set to shuttle-2-turbo, you can change it by passing model="model_name"
        # Default model logic applies to regular, non "ez" functions as well!
        "what is 5 plus 3",  # ez chat auto converts this to a ChatMessage object with role user
    )
    print(response.choices[0].message.content)


    # Same example but streamed
    for message in client.ez_chat(
        "what is 5 plus 3",
        stream=True
    ):
        print(message.choices[0].delta.content, end="", flush=True)


if __name__ == "__main__":
    main()
