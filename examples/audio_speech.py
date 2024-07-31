#!/usr/bin/env python


from shuttleai import ShuttleAI


def main() -> None:

    client = ShuttleAI()

    audio_response = client.audio.speech.generate(
        "hello",
        model="eleven-labs",
        voice="clyde"  # voices listed @ https://api.shuttleai.app/v1/voices
    )

    print(audio_response.data.url)

if __name__ == "__main__":
    main()
