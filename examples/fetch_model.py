#!/usr/bin/env python

from shuttleai.client._sync import ShuttleAIClient
from time import time


def main():
    current = time()
    for _ in range(10):
        client = ShuttleAIClient()

        model = "shuttle-2-turbo"

        model_response = client.fetch_model(model)

        print(model_response)
    print("Time taken: ", time() - current)


if __name__ == "__main__":
    main()