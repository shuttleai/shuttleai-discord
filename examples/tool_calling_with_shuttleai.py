from typing import Any, Callable, Dict, List

import orjson

from shuttleai import ShuttleAI
from shuttleai.helpers import convert_function_json_to_tool_json, serialize_function_to_json
from shuttleai.schemas.chat.completions import ToolCall

# Global registry for functions
tool_registry: Dict[str, Callable] = {}

def register_tool(func: Callable) -> Dict[str, Any]:
    """Register a function as a tool and return its metadata."""
    tool_json = convert_function_json_to_tool_json(serialize_function_to_json(func))
    tool_registry[tool_json["function"]["name"]] = func
    return tool_json

def invoke_tool_calls(tool_calls: List[ToolCall]) -> None:
    """Invoke the tool calls returned by the ShuttleAI API."""
    for tool_call in tool_calls:
        tool_name = tool_call.function.name
        arguments = orjson.loads(tool_call.function.arguments)
        print(f"[*] Invoking tool: {tool_name} with arguments: {arguments}")

        tool_function = tool_registry.get(tool_name)
        if tool_function:
            result = tool_function(**arguments)
            print(f"[!] Tool {tool_name} result: {result}")
        else:
            print(f"[!] Tool {tool_name} not found")

# Dummy Function: In production, this could be your backend API or an external API
def get_current_weather(location: str, unit: str = "fahrenheit") -> str:
    """
    Get the current weather in a given location

    :param location: The city and state, e.g. San Francisco, CA
    :param unit: The unit of temperature to return, either "celsius" or "fahrenheit"
    """
    if "tokyo" in location.lower():
        return orjson.dumps({"location": "Tokyo", "temperature": "10", "unit": unit}).decode()
    elif "san francisco" in location.lower():
        return orjson.dumps({"location": "San Francisco", "temperature": "72", "unit": unit}).decode()
    elif "paris" in location.lower():
        return orjson.dumps({"location": "Paris", "temperature": "22", "unit": unit}).decode()
    else:
        return orjson.dumps({"location": location, "temperature": "unknown"}).decode()


# Register the tools
weather_tool = register_tool(get_current_weather)
tools = [
    weather_tool,
    # Add more tools here
]

# Make the request
shuttleai = ShuttleAI()

response = shuttleai.chat.completions.create(
    model="shuttle-2.5-mini", # our cheapest model, still very capable for high quality completions & tool calling!
    messages=[{"role": "user", "content": "What's the weather like in San Francisco, Paris and Tokyo?"}],
    stream=False,
    tools=tools,
    tool_choice="auto",
)

tool_calls = response.first_choice.message.tool_calls

# Invoke the tool calls
if tool_calls:
    invoke_tool_calls(tool_calls)
else:
    print("No tool calls found in the response")
    print("Text Content:", response.first_choice.message.content)
