import random

from shuttleai import ShuttleAIClient


def main() -> None:
    client = ShuttleAIClient()

    list_models_response = client.list_models()
    print(list_models_response)

    random_model = random.choice(list_models_response.data)
    print("CHOSEN", random_model.id)


if __name__ == "__main__":
    main()
