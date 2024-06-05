from typing import List

from pydantic import BaseModel


class Insult(BaseModel):
    insult: str
    """The insult."""


class InsultResponse(BaseModel):
    data: List[Insult]
    """The list of insults."""
