from typing import List

from pydantic import BaseModel


class Insult(BaseModel):
    insult: str
    """The insult."""


Insults = List[Insult]


class InsultResponse(BaseModel):
    data: Insults
    """The list of insults."""
