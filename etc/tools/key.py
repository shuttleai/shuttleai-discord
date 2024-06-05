import os


def show_key() -> None:
    api_key = os.environ.get("SHUTTLEAI_API_KEY")
    base_url = os.environ.get("SHUTTLEAI_API_BASE", "https://api.shuttleai.app")
    if api_key:
        print(f"Your ShuttleAI API key is: {api_key}")
    else:
        print("No ShuttleAI API key found in environment variables.")

    print(f"Default Base URL (set by SHUTTLEAI_API_BASE env var): {base_url}")
