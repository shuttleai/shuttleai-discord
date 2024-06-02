from shuttleai import ShuttleClient
from shuttleai.schemas import ChatChunk, Chat, ShuttleError
import orjson # [way faster than json](https://github.com/herumes/jsons-benchmark)

shuttleai = ShuttleClient()

print(shuttleai.models)

# chat = shuttleai.chat_completion(
#     model='shuttle-turbo',
#     messages="what is 5 plus 5",
#     stream=True,
#     plain=True,
#     internet=False)

# for completion in chat:
#     print(completion.choices[0].delta.content, end='')