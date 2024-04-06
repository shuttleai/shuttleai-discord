import os
from dotenv import load_dotenv

load_dotenv()

SHUTTLEAI_API_KEY: str = os.getenv('SHUTTLEAI_API_KEY')
DISCORD_BOT_TOKEN: str = os.getenv('DISCORD_BOT_TOKEN')

STREAM_URL: str = os.getenv('STREAM_URL')
STREAM_NAME: str = os.getenv('STREAM_NAME')

MONGO_URI: str = os.getenv('MONGO_URI')

OWNER_IDS: list = list(os.getenv("OWNER_IDS", "206162910848745472,1066613998000291900").split(","))