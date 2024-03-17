from typing import List, Any, Optional
from pydantic import BaseModel

class Item(BaseModel):
    url: str

class Image(BaseModel):
    created: int
    data: List[Item]

class Audio(BaseModel):
    chars: int
    data: List[Item]
    expiresIn: int
    model: str

class Message(BaseModel):
    content: str
    role: str

class Delta(BaseModel):
    content: str

class Choice(BaseModel):
    finish_reason: str
    index: int
    # logprobs: Optional[Dict[str, Any]]
    message: Message

class StreamChoice(BaseModel):
    finish_reason: Optional[str] | None
    index: int 
    # logprobs: Optional[Dict[str, Any]]
    delta: Delta

class Usage(BaseModel):
    completion_tokens: int
    prompt_tokens: int
    total_tokens: int

class ChatChunk(BaseModel):
    id: str
    object: str
    created: int
    model: str
    choices: List[StreamChoice]

class Chat(BaseModel):
    id: str
    object: str
    created: int
    model: str
    choices: List[Choice]
    usage: Usage
    system_fingerprint: str

class Embedding(BaseModel):
    data: List[Any]
    model: str
    obj: str
