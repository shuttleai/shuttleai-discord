#!/usr/bin/env python


from shuttleai import ShuttleAI


def main() -> None:

    client = ShuttleAI()

    audio_response = client.audio.speech.generate(
        input="hello",
        model="eleven_turbo_v2_5",
        voice="clyde"  # voices listed @ https://api.shuttleai.com/v1/voices
    )

    print(audio_response.data.url)

if __name__ == "__main__":
    main()
