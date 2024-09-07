# The Official Python Library for the ShuttleAI API

![Build, Lint, Format](https://img.shields.io/github/actions/workflow/status/shuttleai/shuttleai-python/build_publish.yaml)
[![pypi](https://img.shields.io/pypi/v/shuttleai.svg?color=blue)](https://pypi.org/project/shuttleai/)
[![Downloads](https://pepy.tech/badge/shuttleai)](https://pepy.tech/project/shuttleai)
[![Downloads/Month](https://static.pepy.tech/badge/shuttleai/month)](https://pepy.tech/project/shuttleai)
[![Python Versions](https://img.shields.io/pypi/pyversions/shuttleai.svg)](https://pypi.org/project/shuttleai/)

The ShuttleAI Python library provides easy access to the ShuttleAI REST API for Python 3.9+ applications. It includes type definitions for all request parameters and response fields, offering both synchronous and asynchronous clients powered by [httpx](https://github.com/encode/httpx) and [aiohttp](https://github.com/aio-libs/aiohttp), respectively.

We prioritize performance optimizations across the library. Beyond using orjson for near-instant JSON processing, we implement various techniques to reduce overhead and enhance speed, ensuring efficient and swift API interactions. These optimizations include minimizing built-in library usage, leveraging reusable aiohttp client sessions, and incorporating several small adjustments to streamline operations.

## Installation

```s
pip install shuttleai
```
*We recommend using `--upgrade` or `-U` to ensure you have the latest version of the library.*

### From Source

This client uses `poetry` as a dependency and virtual environment manager.

You can install poetry with

```bash
pip install poetry
```

`poetry` will set up a virtual environment and install dependencies with the following command:

```bash
poetry install
```

## Getting Started

Below is a non-streamed sync and async example for the ShuttleAI API. You can find more examples in the `examples/` directory.

### Synchronous Client

```python
from shuttleai import ShuttleAI

shuttleai = ShuttleAI()

response = shuttleai.chat.completions.create(
    model="shuttle-2.5",
    messages=[{"role": "user", "content": "What day is today?"}],
    internet=True
)

print(chunk.choices[0].message.content)
```

### Asynchronous Client

```python
import asyncio
from shuttleai import AsyncShuttleAI

async def main():
    shuttleai = AsyncShuttleAI()

    response = await shuttleai.chat.completions.create(
        model="shuttle-2.5",
        messages=[{"role": "user", "content": "Imagine an AI like no other, its name is ShuttleAI."}],
    )

    print(response.choices[0].message.content)

asyncio.run(main())
```

### ShuttleAI CLI

Scroll down to the [Scripts](#scripts) section for more information.

## Run examples

You can run the examples in the `examples/` directory using `poetry run` or by entering the virtual environment using `poetry shell`.

### Using poetry run

```bash
cd examples
poetry run python chat_no_streaming.py
```

### Using poetry shell

```bash
poetry shell
cd examples

>> python chat_no_streaming.py
```

## API Key Setup

To use the ShuttleAI API, you need to have an API key. 
You can get a **FREE** API key by signing up at 
[shuttleai.com](https://shuttleai.com) and heading to 
the [key management page](https://shuttleai.com/keys).

After you have an API key, you can set it as an environment variable:

### Windows

```s
setx SHUTTLEAI_API_KEY "<your_api_key>"
```
> [!Note]
> This will only work in the current terminal session. To set it permanently, you can use the `setx` command with the `/m` flag.

```s
setx SHUTTLEAI_API_KEY "<your_api_key>" /m
```

### macOS/Linux

```bash
export SHUTTLEAI_API_KEY=<your_api_key>
```

## Contribution
We welcome and appreciate contributions to the ShuttleAI API Python SDK.
Please see the [contribution guide](CONTRIBUTING.md) for more information.
*Benefits may apply! :smile:*

## Scripts
### Formatting/Checks
- `poetry run ruff check shuttleai` - Check ruff
- `poetry run black shuttleai --diff --color` - Check black
- `poetry run black shuttleai` - Format code
- `poetry run mypy shuttleai` - Check for type errors

### Tools
- `poetry run clean` - Clean up the project directory
- `poetry run key` - Display your default API key (if set by environment variable)
- `poetry run contr` - Display contributors

### ShuttleAI CLI
- `poetry run shuttleai` or `shuttleai` - Run the ShuttleAI CLI.
![Example of Chatbot](https://raw.githubusercontent.com/herumes/githubcdn/main/images/i.png)
![Example response of Chatbot](https://raw.githubusercontent.com/herumes/githubcdn/main/images/i1.png)
> [!Important]
> We support auto TAB completion of commands and model names! Just press `TAB`!
![Example of TAB of Chatbot](https://raw.githubusercontent.com/herumes/githubcdn/main/images/i2.png)
