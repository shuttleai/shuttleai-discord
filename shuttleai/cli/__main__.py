import argparse
import json
import logging
import os
import readline
import sys
from typing import Dict, KeysView, List, Optional, Union

import yaml

from shuttleai import ShuttleAI
from shuttleai.schemas.chat.completions import ChatMessage

MODEL_LIST: List[str] = [
  "shuttleai/shuttle-2.5",
  "shuttle-2-turbo",
  "shuttle-2.5",
  "shuttleai/shuttle-2.5-mini",
  "shuttle-2.5-mini",
  "openai/gpt-4o-mini-2024-07-18",
  "gpt-4o-mini",
  "gpt-4o-mini-2024-07-18",
  "openai/chatgpt-4o-latest",
  "chatgpt-4o",
  "chatgpt-4o-latest",
  "openai/gpt-4o-2024-08-06",
  "gpt-4o-16k",
  "gpt-4o-2024-08-06",
  "openai/gpt-4o-2024-05-13",
  "gpt-4o",
  "gpt-4o-2024-05-13",
  "openai/gpt-4-turbo-2024-04-09",
  "gpt-4-turbo",
  "gpt-4-turbo-2024-04-09",
  "openai/gpt-4-0125-preview",
  "gpt-4-turbo-preview",
  "gpt-4-0125-preview",
  "openai/gpt-4-1106-preview",
  "gpt-4-1106-preview",
  "openai/gpt-4-0613",
  "gpt-4",
  "gpt-4-0613",
  "openai/gpt-3.5-turbo-0125",
  "gpt-3.5-turbo",
  "gpt-3.5-turbo-16k",
  "gpt-3.5-turbo-0125",
  "openai/gpt-3.5-turbo-1106",
  "gpt-3.5-turbo-1106",
  "anthropic/claude-3-5-sonnet-20240620",
  "claude-3-5-sonnet",
  "claude-3.5-sonnet",
  "claude-3-5-sonnet-20240620",
  "anthropic/claude-3-haiku-20240307",
  "claude-3-haiku",
  "claude-3-haiku-20240307",
  "meta-llama/meta-llama-3.1-405b-instruct",
  "llama-3.1-405b",
  "meta-llama-3.1-405b-instruct",
  "meta-llama/meta-llama-3.1-70b-instruct",
  "llama-3.1-70b",
  "meta-llama-3.1-70b-instruct",
  "meta-llama/meta-llama-3.1-8b-instruct",
  "llama-3.1-8b",
  "meta-llama-3.1-8b-instruct"
]
DEFAULT_MODEL: str = "shuttle-2.5"
LOG_FORMAT: str = "%(asctime)s - %(levelname)s - %(message)s"
# A dictionary of all commands and their arguments, used for tab completion.
COMMAND_LIST: Dict[str, Union[Dict[str, Dict], Dict]] = {
    "/new": {},
    "/help": {},
    "/model": {model: {} for model in MODEL_LIST},  # Nested completions for models
    "/system": {},
    "/config": {},
    "/download": {"json": {}, "txt": {}, "yaml": {}},
    "/quit": {},
    "/exit": {},
}

logger = logging.getLogger("chatbot")


def find_completions(
    command_dict: Dict[str, Union[Dict[str, Dict], Dict]], parts: list[str]
) -> Union[KeysView[str], List[str]]:
    if not parts:
        return command_dict.keys()
    if parts[0] in command_dict:
        return find_completions(command_dict[parts[0]], parts[1:])
    else:
        return [cmd for cmd in command_dict if cmd.startswith(parts[0])]


def completer(text: str, state: int) -> Optional[str]:
    buffer = readline.get_line_buffer()  # type: ignore
    line_parts = buffer.lstrip().split(" ")
    options = find_completions(COMMAND_LIST, line_parts[:-1])

    try:
        return [option for option in options if option.startswith(line_parts[-1])][state]
    except IndexError:
        return None


readline.set_completer(completer)  # type: ignore
readline.set_completer_delims(" ")  # type: ignore
# Enable tab completion
readline.parse_and_bind("tab: complete")  # type: ignore


class ChatBot:
    def __init__(self, api_key: str, model: str, system_message: Optional[str] = None):
        if not api_key:
            raise ValueError("An API key must be provided to use the ShuttleAI API.")
        self.client = ShuttleAI(api_key=api_key)
        self.model = model
        self.system_message = system_message
        self.messages: List[ChatMessage] = []

    def opening_instructions(self) -> None:
        print(
            """
To chat: type your message and hit enter
To start a new chat: /new
To switch model: /model <model name>
To switch system message: /system <message>
To see current config: /config
To exit: /exit, /quit, or hit CTRL+C
To see this help: /help
HINT: We support TAB autocompletion for commands and model names!
"""
        )

    def new_chat(self) -> None:
        print("")
        print(f"Starting new chat with model: \033[38;5;105m{self.model}\033[0m")
        print("")
        self.messages = []
        if self.system_message:
            self.messages.append(ChatMessage(role="system", content=self.system_message))

    def switch_model(self, input: str) -> None:
        model = self.get_arguments(input)
        if model in MODEL_LIST:
            self.model = model
            logger.info(f"\033[38;5;105m{model}\033[")
        else:
            logger.error(f"Invalid model name: {model}")

    def switch_system_message(self, input: str) -> None:
        system_message = self.get_arguments(input)
        if system_message:
            self.system_message = system_message
            logger.info(f"Switching system message: {system_message}")
            self.new_chat()
        else:
            logger.error(f"Invalid system message: {system_message}")

    def show_config(self) -> None:
        print("")
        print(f"Current model: \033[38;5;105m{self.model}\033[0m")
        print(f"Current system message: {self.system_message}")
        print("")

    def collect_user_input(self) -> str:
        print("")
        return input("\033[38;2;50;168;82mUser: \033[0m")

    def run_inference(self, content: str) -> None:
        print("")
        print("\033[38;5;105mSHUTTLEAI\033[0m:")
        print("")

        self.messages.append(ChatMessage(role="user", content=content))

        assistant_response = ""
        logger.debug(f"Running inference with model: {self.model}")
        logger.debug(f"Sending messages: {self.messages}")
        for chunk in self.client.chat.completions.create(model=self.model, messages=self.messages, stream=True):
            response = chunk.choices[0].delta.content
            if response is not None:
                print(response, end="", flush=True)
                assistant_response += response

        print("", flush=True)

        if assistant_response:
            self.messages.append(ChatMessage(role="assistant", content=assistant_response))
        logger.debug(f"Current messages: {self.messages}")

    def get_command(self, input: str) -> str:
        return input.split()[0].strip()

    def get_arguments(self, input: str) -> str:
        try:
            return " ".join(input.split()[1:])
        except IndexError:
            return ""

    def is_command(self, input: str) -> bool:
        return self.get_command(input) in COMMAND_LIST

    def execute_command(self, input: str) -> None:
        command = self.get_command(input)
        if command in ["/exit", "/quit"]:
            self.exit()
        elif command == "/help":
            self.opening_instructions()
        elif command == "/new":
            self.new_chat()
        elif command == "/model":
            self.switch_model(input)
        elif command == "/system":
            self.switch_system_message(input)
        elif command == "/config":
            self.show_config()
        elif command == "/download":
            self.download_conversation(input)

    def download_conversation(self, input: str) -> None:
        format = self.get_arguments(input).lower()
        if format not in ["json", "txt", "yaml"]:
            logger.error("Invalid format. Choose from 'json', 'txt', or 'yaml'.")
            return

        filename = f"conversation.{format}"
        try:
            if format == "json":
                with open(filename, "w") as f:
                    json.dump([msg.model_dump(exclude_none=True) for msg in self.messages], f, indent=4)
            elif format == "txt":
                with open(filename, "w") as f:
                    for msg in self.messages:
                        f.write(f"{msg.role.capitalize()}: {msg.content}\n\n")
            elif format == "yaml":
                with open(filename, "w") as f:
                    yaml.dump([msg.model_dump(exclude_none=True) for msg in self.messages], f, default_flow_style=False)
            logger.info(f"Conversation saved to {filename}")
        except Exception as e:
            logger.error(f"Error saving conversation: {e}")

    def start(self) -> None:
        self.opening_instructions()
        self.new_chat()
        while True:
            try:
                input = self.collect_user_input()
                if self.is_command(input):
                    self.execute_command(input)
                else:
                    self.run_inference(input)

            except KeyboardInterrupt:
                self.exit()

    def exit(self) -> None:
        logger.debug("Exiting chatbot")
        sys.exit(0)


def main() -> None:
    parser = argparse.ArgumentParser(description="A simple chatbot using the ShuttleAI API")
    parser.add_argument(
        "--api-key",
        default=os.environ.get("SHUTTLEAI_API_KEY"),
        help="ShuttleAI API key. Defaults to environment variable SHUTTLEAI_API_KEY",
    )
    parser.add_argument(
        "-m",
        "--model",
        choices=MODEL_LIST,
        default=DEFAULT_MODEL,
        help="Model for chat inference. Choices are %(choices)s. Defaults to %(default)s",
    )
    parser.add_argument("-s", "--system-message", help="Optional system message to prepend.")
    parser.add_argument("-d", "--debug", action="store_true", help="Enable debug logging")

    args = parser.parse_args()

    if args.debug:
        logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.INFO)

    formatter = logging.Formatter(LOG_FORMAT)

    ch = logging.StreamHandler()
    ch.setFormatter(formatter)
    logger.addHandler(ch)

    logger.debug(f"Starting chatbot with model: {args.model}, " f"system message: {args.system_message}")

    try:
        bot = ChatBot(args.api_key, args.model, args.system_message)
        bot.start()
    except Exception as e:
        logger.error(e)
        sys.exit(1)


if __name__ == "__main__":
    main()
