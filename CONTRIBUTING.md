# Contributing to ShuttleAI

Thank you for your interest in contributing to the ShuttleAI project! We welcome contributions of all kinds, including bug reports, feature requests, documentation improvements, and code contributions.

*We are in the midst of remaking the wrapper, your help with adding previous endpoints to the new wrapper is needed!*

The ShuttleAI Python SDK uses poetry as previously discussed, on top of this, we use [ruff](https://github.com/astral-sh/ruff) for linting and formatting as well as [mypy](https://github.com/python/mypy) for type checking. Please ensure that your code passes all of these checks before submitting a pull request expecting to be merged.

## Lazy Contributing

If you're feeling lazy and don't want to go through the necessary checks such as linting and type checking, you may still submit a pull request. However, it will be marked as `WIP` and will not be merged until all checks have passed. This is to ensure that the codebase remains consistent and clean.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [How to Contribute](#how-to-contribute)
  - [Reporting Bugs](#reporting-bugs)
  - [Suggesting Features](#suggesting-features)
  - [Improving Documentation](#improving-documentation)
  - [Contributing Code](#contributing-code)
- [Development Setup](#development-setup)
  - [Forking the Repository](#forking-the-repository)
  - [Cloning Your Fork](#cloning-your-fork)
  - [Setting Up the Environment](#setting-up-the-environment)
  - [Running Checks](#running-checks)
  - [Running Tests](#running-tests)
- [Submitting Changes](#submitting-changes)
  - [Commit Messages](#commit-messages)
  - [Pull Requests](#pull-requests)
- [Community](#community)

## Code of Conduct

This project adheres to the Contributor Covenant [Code of Conduct](CODE_OF_CONDUCT.md). By participating, you are expected to uphold this code. Please report unacceptable behavior to [email@example.com](mailto:email@example.com).

## How to Contribute

### Reporting Bugs

If you find a bug, please open an issue on GitHub with as much detail as possible. Include steps to reproduce the bug, the expected behavior, and what actually happens.

### Suggesting Features

We welcome feature suggestions! Please open an issue on GitHub with a clear and detailed description of the feature you would like to see, including any potential use cases.

### Improving Documentation

Improving documentation is a valuable way to contribute. If you find any part of the documentation unclear or incomplete, feel free to make changes and submit a pull request.

### Contributing Code

If you are interested in contributing code, please follow the guidelines below.

## Development Setup

### Forking the Repository

First, fork the repository to your GitHub account.

### Cloning Your Fork

Clone your forked repository to your local machine:

```sh
git clone https://github.com/your-username/shuttleai.git
cd shuttleai
```

### Setting Up the Environment

We use [poetry](https://python-poetry.org/) to manage dependencies. To install poetry, run the following command:

```sh
pip install poetry
```

Next, install the dependencies:

```sh
poetry install
```

### Running Checks

We use [ruff](https://github.com/astral-sh/ruff) for linting and formatting as well as [mypy](https://github.com/python/mypy) for type checking. To run all checks, run the following command:

```sh
poetry run ruff format . --check && poetry run mypy .
```

### Running Tests

We use [pytest](https://docs.pytest.org/en/latest/) for testing. To run all tests, run the following command:

```sh
poetry run pytest .
```

> [!IMPORTANT]
> The tests will fail if the API key is not set. To set the API key, create a file called `.env` in the root of the project and add the following line:
> ```sh
> SHUTTLEAI_API_KEY=your-api-key
> ```


## Submitting Changes

### Commit Messages

We recommend the [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/) specification for commit messages.

### Pull Requests

When submitting a pull request, please make sure to:

- Write a clear and descriptive title for the pull request.
- Include as much detail as possible in the pull request description. This should include a summary of the changes, the motivation for the changes, and any potential side effects.
- Link to any relevant issues or pull requests.
- Make sure all checks pass.

## Community

If you have any questions, feel free to reach out to us on [Discord](https://discord.gg/shuttleai) or you may contact one of the main project [maintainers](https://github.com/shuttleai/shuttleai-python/graphs/contributors).
