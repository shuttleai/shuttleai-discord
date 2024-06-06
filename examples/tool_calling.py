#!/usr/bin/env python


from typing import Any

import orjson

from shuttleai import ShuttleAI
from shuttleai.helpers import (
    convert_function_json_to_tool_json,
    serialize_function_to_json,
)
from shuttleai.schemas.chat.completions import ChatMessage, FunctionCall


def get_current_weather(location: str, unit: str = "fahrenheit") -> str:
    """
    Get the current weather in a given location

    :param location: The city and state, e.g. San Francisco, CA
    :param unit: The unit of temperature to return, either "celsius" or "fahrenheit"
    """
    temperature = 80
    return str(temperature) + " degrees " + unit[0].upper()


get_current_weather_tool = convert_function_json_to_tool_json(serialize_function_to_json(get_current_weather))
# ShuttleAI supports function/tool calling helpers to easily serialize a function (formatted as above) to a tool JSON.
#                                                           ^ & deserialize a function from a tool JSON.


tools = [get_current_weather_tool]

def invoke_function_call(function: FunctionCall) -> Any | None:
    if function.name in globals():
        return globals()[function.name](**(orjson.loads(function.arguments)))
    return None

history = [
    ChatMessage(role="user", content="what is the weather in scotland? please tell me in fahrenheit")
]

def main() -> None:
    model = "shuttle-2-turbo"

    client = ShuttleAI()

    chat_response = client.chat.completions.create(
        model=model,
        messages=history,
        tools=tools,
        tool_choice="auto"
    )

    message = chat_response.choices[0].message
    print(message)
    tool_calls = message.tool_calls
    assert tool_calls is not None and len(tool_calls) > 0 # We expect at least one tool call
    first_tool_call = tool_calls[0]
    function_call = first_tool_call.function

    result = invoke_function_call(function_call)

    print(result)

    # history.append(ChatMessage(role="tool", content=result, tool_call_id=first_tool_call.id, name=function_call.name))
    history.append(
        ChatMessage(role="system", content=f"The result to the user's query is: '{result}'. Anser using this info.")
    )

    chat_response_2 = client.chat.completions.create(
        model=model,
        messages=history,
    )

    print(chat_response_2.choices[0].message)



if __name__ == "__main__":
    main()
