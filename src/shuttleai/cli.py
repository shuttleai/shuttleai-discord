import asyncclick as click
import os

import pystyle
from pystyle import Colors, Colorate, Box

from .log import log, TerminalColor
from .shuttleai_async import ShuttleAsyncClient

# os.environ['SHUTTLE_AI_API_KEY'] = "shuttle-YOUR-KEY"

BANNER = r"""
   _____ _           _   _   _               _____ 
  / ____| |         | | | | | |        /\   |_   _|
 | (___ | |__  _   _| |_| |_| | ___   /  \    | |  
  \___ \| '_ \| | | | __| __| |/ _ \ / /\ \   | |  
  ____) | | | | |_| | |_| |_| |  __// ____ \ _| |_ 
 |_____/|_| |_|\__,_|\__|\__|_|\___/_/    \_\_____|

 """
BOX_BANNER = Box.DoubleCube(BANNER)
COLOR_BANNER = Colorate.Vertical(Colors.blue_to_purple, BOX_BANNER, 1)

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

@click.group()
def shuttleai_cli():
    pass

@shuttleai_cli.command()
@click.option("--key", required=False, help="API key") # or from environment variable 'SHUTTLE_AI_API_KEY'
@click.option('--model', required=False, help='Model name', default='shuttle-turbo') # default to 'shuttle-turbo'
@click.option('--system', required=True, help='System Prompt', default="You are ShuttleAI, the world's best, smartest, fastest, and most concise developer. You are the best AI coder in the world.")
@click.option('--stream', is_flag=True, help='Stream mode', default=True)
async def chat(key, model, system, stream):
    sub_commands = ['!clear', '!exit']

    key = key or os.environ.get('SHUTTLE_AI_API_KEY') or click.prompt('[Warning]: The `SHUTTLE_AI_API_KEY` environment variable is not set!\nPlease enter your API key', hide_input=True)
    masked_key = (key[:11] + "*" * (len(key) - 11))
    log.info(f"[KEY]: {masked_key}")

    log.info(f"Chatting with [{model}]:")
    log.info(f"Available sub commands: {sub_commands}")

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

        async with ShuttleAsyncClient(key, 120) as shuttle:
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
    print(COLOR_BANNER)
    shuttleai_cli()

if __name__ == '__main__':
    main()
