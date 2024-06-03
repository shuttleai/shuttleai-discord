from shuttleai import ShuttleAIClient


def main() -> None:
    client = ShuttleAIClient()

    model = "shuttle-2-turbo"

    model_response = client.fetch_model(model)

    print(model_response)


if __name__ == "__main__":
    main()
