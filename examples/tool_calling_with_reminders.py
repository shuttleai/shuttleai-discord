import threading
import time
from typing import Any, Dict, List

import orjson

from shuttleai import ShuttleAI
from shuttleai.helpers import convert_function_json_to_tool_json, serialize_function_to_json
from shuttleai.schemas.chat.completions import ToolCall

shuttleai = ShuttleAI()

def set_reminder(message: str, duration: int) -> str:
    """
    Set a reminder for the user.

    :param message: The reminder message
    :param duration: The duration in seconds after which to remind the user
    """
    def reminder_thread() -> None:
        time.sleep(duration)
        print(f"**REMINDER**: {message}", flush=True)

    threading.Thread(target=reminder_thread).start()
    return f"Reminder set: '{message}' in {duration} seconds"

if __name__ == "__main__":
    while True:
        prompt = input("You: ")
        # prompt = "please set a reminder for 30 seconds telling me to get up and do my laundry"

        messages = [
            {"role": "system", "content": (
                "You are a helpful assistant with the ability to set real-time reminders. "
                "Never assume what to plug into function call arguments, always ask the user for the necessary information. "
                "After setting the reminder and receiving the tool role response, "
                "tell the user their reminder has been set and ask them if they need anything else while they wait. "
                "When not invoking these functions/tools, reply as normal. Be helpful and friendly."
            )},
            {"role": "user", "content": prompt}
        ]
        tools = [convert_function_json_to_tool_json(serialize_function_to_json(set_reminder))]
        response = shuttleai.chat.completions.create(
            model="shuttle-3-mini",
            messages=messages,
            tools=tools,
            tool_choice="auto"
        )
        response_f = response.first_choice.message
        if response_f.tool_calls:
            tool_calls: List[ToolCall] = response_f.tool_calls

            for tool_call in tool_calls:
                function_call = tool_call.function
                if function_call.name == "set_reminder":
                    arguments: Dict[str, Any] = orjson.loads(function_call.arguments)
                    reminder_response = set_reminder(**arguments)
                    print(reminder_response)
                    messages.append({
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "name": function_call.name,
                        "content": reminder_response
                    })
        elif response_f.content:
            messages.append({"role": "assistant", "content": response_f.content})
            print(response_f.content)
        else:
            print(messages)
            print("No answer found.")
