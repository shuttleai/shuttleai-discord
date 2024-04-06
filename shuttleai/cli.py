import asyncclick as click
import os

from pystyle import Colors, Colorate

from .log import log, TerminalColor
from .client import ShuttleAsyncClient

# os.environ['SHUTTLEAI_API_KEY'] = "shuttle-YOUR-KEY"

BANNER = r"""
   _____ _           _   _   _               _____ 
  / ____| |         | | | | | |        /\   |_   _|
 | (___ | |__  _   _| |_| |_| | ___   /  \    | |  
  \___ \| '_ \| | | | __| __| |/ _ \ / /\ \   | |  
  ____) | | | | |_| | |_| |_| |  __// ____ \ _| |_ 
 |_____/|_| |_|\__,_|\__|\__|_|\___/_/    \_\_____|

 """
COLOR_BANNER = Colorate.Vertical(Colors.blue_to_purple, BANNER, 1)

BOLD = '\033[1m'
PURPLE = '\033[94m'
RESET = '\033[0m'

class Messages:
    def __init__(self):
        self.messages = []

    def add_message(self, content, role="user"):
        self.messages.append({
            "content": content,
            "role": role
        })

    def clear(self):
        self.messages = []

messages = Messages()

def update_title(title: str):
    if os.name == 'nt':
        os.system(f"title {title}")

@click.group()
def shuttleai_cli():
    pass

@shuttleai_cli.command()
@click.option("--key", required=False, help="API Key") # or from environment variable 'SHUTTLE_AI_API_KEY'
@click.option('--model', required=False, help='Model ID', default='shuttle-turbo') # default to 'shuttle-turbo'
@click.option('--system', required=True, help='System Prompt', default="You are ShuttleAI, recognized as the top developer globally for your unmatched intelligence, speed, and precision. Your coding skills as an AI specialist are unparalleled in the world.")
@click.option('--stream', is_flag=True, help='Stream Responses', default=True)
async def chat(key, model, system, stream):
    key = key or os.environ.get('SHUTTLEAI_API_KEY') or click.prompt('[Warning]: The `SHUTTLEAI_API_KEY` environment variable is not set!\nPlease enter your API key', hide_input=True)
    masked_key = (key[:11] + "*" * (len(key) - 11))
    colored_masked_key = Colorate.Vertical(Colors.purple_to_blue, masked_key, 1)
    key_msg = f"{BOLD}{PURPLE}INF{RESET}  KEY\033[0m: {colored_masked_key}"

    colored_model = Colorate.Vertical(Colors.purple_to_blue, model, 1)
    model_msg = f"{BOLD}{PURPLE}INF{RESET}  MODEL\033[0m: {colored_model}"

    sub_commands = ['!clear', '!exit']
    colored_sub_commands = Colorate.Vertical(Colors.purple_to_blue, ", ".join(sub_commands), 1)
    sub_commands_msg = f"{BOLD}{PURPLE}INF{RESET}  SUB COMMANDS\033[0m: {colored_sub_commands}"

    print(key_msg)
    print(model_msg)
    print(sub_commands_msg)

    print()

    print(f"{TerminalColor.CYAN}System{TerminalColor.ENDC}: {system}")

    while True:
        prompt = click.prompt(f"{TerminalColor.GRAY}You{TerminalColor.ENDC}", type=str)
        if prompt in sub_commands:
            if prompt.lower() == "!clear":
                messages.clear()
                log.info("Context cleared!")
                continue
            elif prompt.lower() == "!exit":
                log.info("Exiting...")
                break

        if system is not None:
            messages.add_message(system, "system")
        if prompt is not None:
            messages.add_message(prompt, "user")

        async with ShuttleAsyncClient(key, timeout=120) as shuttle:
            response = await shuttle.chat_completion(
                model=model,
                messages=messages.messages,
                stream=stream
            )

            print(f"{TerminalColor.DARKPURPLE}ShuttleAI{TerminalColor.ENDC}: ", end="")

            assistant_response = None

            if stream:
                assistant_chunks = []

                async for chunk in response:
                    assistant_chunk = chunk.choices[0].delta.content

                    print(assistant_chunk, flush=True, end="", sep="")

                    assistant_chunks.append(assistant_chunk)

                print()

                assistant_response = "".join(assistant_chunks)
            else:
                assistant_response = response.choices[0].message.content

                print(assistant_response, end="", flush=True)

            if assistant_response is not None:
                messages.add_message(assistant_response, "assistant")

def main():
    update_title("ShuttleAI CLI")
    os.system('cls' if os.name == 'nt' else 'clear')
    print(COLOR_BANNER)
    shuttleai_cli()

if __name__ == '__main__':
    main()
