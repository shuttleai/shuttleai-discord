# Contributing to ShuttleAI

Thank you for considering contributing to the ShuttleAI project! Your contributions, whether bug reports, feature requests, documentation improvements, or code, are invaluable.

**We need your help with adding previous endpoints to the new wrapper!**

The ShuttleAI Python SDK uses [poetry](https://python-poetry.org/), [ruff](https://github.com/astral-sh/ruff) for linting and formatting, and [mypy](https://github.com/python/mypy) for type checking. Ensure your code passes all checks before submitting a pull request.

## Benefits
Top contributors receive a special role in the [ShuttleAI Discord Server](https://discord.gg/shuttleai).

![Example of a contributor with a special role](https://cdn.discordapp.com/attachments/1181912564553232444/1246701293523828817/image.png?ex=665d588e&is=665c070e&hm=5f0d1bfad1fbfad95076de6dc8616c177cd73d548c99537c5901d959121c42c8&)

## Lazy Contributing
You can submit a pull request without passing checks, but it will be marked as `WIP` and not merged until all checks pass.

## Table of Contents
- [Code of Conduct](#code-of-conduct)
- [How to Contribute](#how-to-contribute)
  - [Reporting Bugs](#reporting-bugs)
  - [Suggesting Features](#suggesting-features)
  - [Improving Documentation](#improving-documentation)
  - [Contributing Code](#contributing-code)
- [Development Setup](#development-setup)
- [Submitting Changes](#submitting-changes)
- [Community](#community)

## Code of Conduct
This project adheres to the Contributor Covenant [Code of Conduct](CODE_OF_CONDUCT.md). Report unacceptable behavior to [the ShuttleAI team](mailto:chris@shuttleai.app).

## How to Contribute

### Reporting Bugs
Open an issue on GitHub with detailed steps to reproduce, expected behavior, and actual behavior.

### Suggesting Features
Open an issue on GitHub with a clear and detailed description of the feature and potential use cases.

### Improving Documentation
If you find unclear or incomplete documentation, make changes and submit a pull request.

### Contributing Code
Follow the development setup and submission guidelines below.

## Development Setup

### Fork and Clone
Fork the repository and clone it to your local machine:
```sh
git clone https://github.com/your-username/shuttleai.git
cd shuttleai
```

### Set Up the Environment
Install [poetry](https://python-poetry.org/):
```sh
pip install poetry
poetry install
```

### Running Checks
Run linting and type checking:
```sh
poetry run ruff format . --check && poetry run mypy .
```

### Running Tests
Run tests with [pytest](https://docs.pytest.org/en/latest/):
```sh
poetry run pytest .
```
Ensure you set the API key in a `.env` file:
```sh
SHUTTLEAI_API_KEY=your-api-key
```

## Submitting Changes

### Commit Messages
Follow the [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/) specification.

### Pull Requests
When submitting a pull request:
- Write a clear and descriptive title.
- Include a detailed description of the changes, motivation, and potential side effects.
- Link relevant issues or pull requests.
- Ensure all checks pass.

## Community
For questions, reach out on [Discord](https://discord.gg/shuttleai) or contact the [maintainers](https://github.com/shuttleai/shuttleai-python/graphs/contributors).