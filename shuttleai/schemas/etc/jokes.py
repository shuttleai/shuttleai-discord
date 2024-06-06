from typing import List

from pydantic import BaseModel


class Joke(BaseModel):
    joke: str
    """The joke."""


class JokeResponse(BaseModel):
    data: List[Joke]
    """The list of jokes."""
