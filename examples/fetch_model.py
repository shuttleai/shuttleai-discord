#!/usr/bin/env python


from shuttleai import ShuttleAI


def main() -> None:
    client = ShuttleAI()

    model = "shuttle-2-turbo"

    model_response = client.fetch_model(model)

    print(model_response)


if __name__ == "__main__":
    main()
