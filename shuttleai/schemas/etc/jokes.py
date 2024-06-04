from typing import List

from pydantic import BaseModel


class Joke(BaseModel):
    joke: str
    """The joke."""


Jokes = List[Joke]


class JokeResponse(BaseModel):
    data: Jokes
    """The list of jokes."""
