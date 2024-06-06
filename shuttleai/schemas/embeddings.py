from typing import List

from pydantic import BaseModel

from shuttleai.schemas.common import UsageInfo


class EmbeddingObject(BaseModel):
    object: str
    embedding: List[float]
    index: int


class EmbeddingResponse(BaseModel):
    object: str
    data: List[EmbeddingObject]
    model: str
    usage: UsageInfo
