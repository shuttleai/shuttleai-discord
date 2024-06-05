#!/usr/bin/env python


import random

from shuttleai import ShuttleAIClient
from shuttleai.schemas.models.models import VerboseModelCard


def main() -> None:
    client = ShuttleAIClient()

    list_models_response = client.list_models_verbose()
    print(list_models_response)

    random_model = random.choice(list_models_response.data)
    assert isinstance(random_model, VerboseModelCard), "You got a proxy object!."
    print("CHOSEN", random_model.name)


if __name__ == "__main__":
    main()
