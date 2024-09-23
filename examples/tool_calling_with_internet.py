from typing import Any, Dict, List

import orjson

from shuttleai import ShuttleAI
from shuttleai.helpers import convert_function_json_to_tool_json, serialize_function_to_json
from shuttleai.schemas.chat.completions import ToolCall

shuttleai = ShuttleAI()

def web_search(query: str) -> str:
    """
    A live real-time web search function that searches Google for the given query.

    :param query: The search query
    """
    response = shuttleai.web.search(query).model_dump()
    return orjson.dumps(response["data"]).decode()


if __name__ == "__main__":
    prompt = "When did the Five Nights at Freddy's Movie release?"

    messages = [{"role": "user", "content": prompt}]
    tools = [convert_function_json_to_tool_json(serialize_function_to_json(web_search))]
    trigger_response = shuttleai.chat.completions.create(
        model="shuttle-2.5",
        messages=messages,
        tools=tools,
        tool_choice="auto"
    )

    trigger_first = trigger_response.first_choice.message
    if trigger_first.tool_calls:
        tool_calls: List[ToolCall] = trigger_first.tool_calls

        for tool_call in tool_calls:
            function_call = tool_call.function
            if function_call.name == "web_search":
                arguments: Dict[str, Any] = orjson.loads(function_call.arguments)
                web_response = web_search(**arguments)
                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "name": function_call.name,
                    "content": web_response
                })

        answer_response = shuttleai.chat.completions.create(
            model="shuttle-2.5",
            messages=messages
        )
        answer_content = answer_response.first_choice.message.content
        if answer_content:
            messages.append({"role": "assistant", "content": answer_content})

            print(answer_content)
        else:
            print(messages)
            print("No answer found.")
    else:
        print("No tool calls found.")
        print(trigger_first.content)