from typing import List, Any, Optional
from pydantic import BaseModel

class ShuttleModel(BaseModel):
    id: str
    object: str
    owned_by: str
    created: int
    cost: int
    premium: Optional[bool] = None
    tokens: Optional[int] = None
    info: Optional[str] = None
    max_images: Optional[int] = None
    multiple_of: Optional[int] = None
    maintenance: Optional[bool] = None
    beta: Optional[bool] = None
    voices: Optional[str] = None
    file_upload: Optional[bool] = None
    proxy_to: Optional[str] = None
    endpoint: str

class Error(BaseModel):
    message: str
    type: str
    param: Optional[str] = None
    code: Optional[str] = None
    hint: Optional[str] = None

class ShuttleError(BaseModel):
    error: Error
    status: int
    docs: str

class Models(BaseModel):
    object: str
    data: List[ShuttleModel]
    total: int

class Model(BaseModel):
    object: str
    data: ShuttleModel

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
    finish_reason: Optional[str] = None
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
