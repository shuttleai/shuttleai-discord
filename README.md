# The Official Python library for the ShuttleAI API

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
[shuttleai.app](https://shuttleai.app) and heading to 
the [key management page](https://shuttleai.app/keys).

After you have an API key, you can set it as an environment variable:

### Windows

```s
setx SHUTTLEAI_API_KEY "<your_api_key>"
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
- `poetry run ruff check shuttleai` - Check for code formatting issues
- `poetry run black shuttleai --diff --color` - Check for code formatting issues
- `poetry run black shuttleai` - Format code
- `poetry run mypy shuttleai` - Check for type errors

### Tools
- `poetry run clean` - Clean up the project directory
- `poetry run key` - Display your default API key (if set by environment variable)
- `poetry run contributors` - Display contributors

### Interactive Chatbot
- `poetry run shuttleai` - Run the interactive chatbot
