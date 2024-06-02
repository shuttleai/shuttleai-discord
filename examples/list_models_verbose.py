#!/usr/bin/env python

import random

from shuttleai.client._sync import ShuttleAIClient


def main():
    client = ShuttleAIClient()

    list_models_response = client.list_models_verbose()
    print(list_models_response)

    random_model = random.choice(list_models_response.data)
    print("CHOSEN", random_model.name)


if __name__ == "__main__":
    main()
