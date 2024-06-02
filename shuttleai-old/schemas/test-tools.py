from shuttleai import ShuttleClient
from shuttleai.schemas import ChatChunk, Chat, ShuttleError
from shuttleai.helpers.tool_calls import serialize_function_to_json, deserialize_function_from_json
from typing import Literal
import orjson # [way faster than json](https://github.com/herumes/jsons-benchmark)
import random


def get_current_weather(location: str, unit: Literal["celsius", "fahrenheit"] = "fahrenheit") -> str:
    """
    Get the current weather in a given location

    :param location: The city and state, e.g. San Francisco, CA
    :param unit: The unit of temperature to return, either "celsius" or "fahrenheit"
    """
    temperature = random.randint(-10, 40) if unit == "celsius" else random.randint(14, 104)
    return str(temperature) + "°" + unit[0].upper()

get_current_weather_tool = serialize_function_to_json(get_current_weather)

tools = [get_current_weather_tool]

shuttleai = ShuttleClient()

chat = shuttleai.chat_completion(
    model='gpt-3.5-turbo',
    messages="what is the weather in paris",
    plain=True,
    tools=tools,
    tool_choice="auto"
    )

print(chat.choices[0].message, end='')