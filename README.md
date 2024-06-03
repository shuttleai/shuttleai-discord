# The Official Python library for the ShuttleAI API

[![pypi](https://img.shields.io/pypi/v/shuttleai.svg?color=blue)](https://pypi.org/project/shuttleai/)
[![Downloads](https://pepy.tech/badge/shuttleai)](https://pepy.tech/project/shuttleai)
[![Downloads/Month](https://static.pepy.tech/badge/shuttleai/month)](https://pepy.tech/project/shuttleai)
[![Python Versions](https://img.shields.io/pypi/pyversions/shuttleai.svg)](https://pypi.org/project/shuttleai/)

The ShuttleAI Python library provides convenient access to the ShuttleAI REST API from any Python 3.9+ application. The library includes type definitions for all request params and response fields, and offers both synchronous and asynchronous clients powered by [httpx](https://github.com/encode/httpx) and [aiohttp](https://github.com/aio-libs/aiohttp) respectively.

We took this dynamic change from pure httpx to ensure we get the performance benefits of re usable aiohttp client sessions.

*A future plan may be to replace httpx with requests/niquests for the synchronous client*

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
We welcome contributions to the ShuttleAI API Python SDK.
Please see the [contribution guide](CONTRIBUTING.md) for more information.
