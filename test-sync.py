from src.shuttleai import ShuttleClient
from src.shuttleai.schemas import ChatChunk, Chat, ShuttleError
import orjson # [way faster than json](https://github.com/herumes/jsons-benchmark)

shuttleai = ShuttleClient()

chat = shuttleai.chat_completion(
    model='shuttle-turbo',
    messages="write discord.py bot code",
    stream=True,
    plain=True,
    internet=False)

for completion in chat:
    print(completion.choices[0].delta.content, end='')