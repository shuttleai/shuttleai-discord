# The Official Python Wrapper for the ShuttleAI API

Access the ShuttleAI API with an easy-to-use user-friendly lib.

[![pypi](https://img.shields.io/pypi/v/shuttleai.svg?color=blue)](https://pypi.org/project/shuttleai/)
[![Downloads](https://pepy.tech/badge/shuttleai)](https://pepy.tech/project/shuttleai)
[![License](https://img.shields.io/pypi/l/shuttleai.svg)](https://pypi.org/project/shuttleai/)
[![Python Versions](https://img.shields.io/pypi/pyversions/shuttleai.svg)](https://pypi.org/project/shuttleai/)

## Installation

```sh
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

```bash
export SHUTTLEAI_API_KEY=<your_api_key>
```


## Contribution
We welcome contributions to the ShuttleAI API Python SDK.
Please see the [contribution guide](CONTRIBUTING.md) for more information.
