import os


def show_key() -> None:
    api_key = os.environ.get("SHUTTLEAI_API_KEY")
    if api_key:
        print(f"Your ShuttleAI API key is: {api_key}")
    else:
        print("No ShuttleAI API key found in environment variables.")
