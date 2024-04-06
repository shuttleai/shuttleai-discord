from typing import List, Any, Optional
from dataclasses import dataclass

@dataclass
class ShuttleModel:
    id: str
    object: str
    owned_by: str
    created: int
    cost: int
    endpoint: str
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

@dataclass
class Error:
    message: str
    type: str
    param: Optional[str] = None
    code: Optional[str] = None
    hint: Optional[str] = None

@dataclass
class ShuttleError:
    error: Error
    status: int
    docs: str
    input: Optional[dict] = None
    request_id: Optional[str] = None

@dataclass
class Models:
    object: str
    data: List[ShuttleModel]
    total: int

    @classmethod
    def from_dict(cls, data: dict) -> 'Models':
        return cls(object=data['object'], data=[ShuttleModel(**model) for model in data['data']], total=data['total'])

@dataclass 
class Model:
    object: str
    data: ShuttleModel

@dataclass
class Item:
    url: str

@dataclass
class Image:
    created: int
    data: List[Item]
    model: str

    @classmethod
    def from_dict(cls, data: dict) -> 'Image':
        return cls(created=data['created'], data=[Item(**item) for item in data['data']], model=data['model'])

@dataclass
class Audio:
    chars: int
    data: List[Item]
    expiresIn: int
    model: str

    @classmethod
    def from_dict(cls, data: dict) -> 'Audio':
        return cls(chars=data['chars'], data=[Item(**item) for item in data['data']], expiresIn=data['expiresIn'], model=data['model'])

@dataclass
class Message:
    content: str
    role: str

    @classmethod
    def from_dict(cls, data: dict) -> 'Message':
        return cls(**data)

@dataclass
class Delta:
    role: str
    content: str

    @classmethod
    def from_dict(cls, data: dict) -> 'Delta':
        return cls(**data)

@dataclass
class Choice:
    finish_reason: str
    index: int
    message: Message

    @classmethod
    def from_dict(cls, data: dict) -> 'Choice':
        message_data = data.get('message', {})
        message = Message.from_dict(message_data)
        return cls(finish_reason=data['finish_reason'], index=data['index'], message=message)

@dataclass
class StreamChoice:
    index: int
    delta: Delta
    finish_reason: Optional[str] = None

    @classmethod
    def from_dict(cls, data: dict) -> 'StreamChoice':
        delta_data = data.get('delta', {})
        delta = Delta.from_dict(delta_data)
        return cls(index=data['index'], delta=delta, finish_reason=data.get('finish_reason', None))

@dataclass 
class Usage:
    completion_tokens: int
    prompt_tokens: int
    total_tokens: int

@dataclass
class ChatChunk:
    id: str
    object: str
    created: int
    model: str
    choices: List[StreamChoice]

    @classmethod
    def from_dict(cls, data: dict) -> 'ChatChunk':
        choices_data = data.get('choices', [])
        choices = [StreamChoice.from_dict(choice_data) for choice_data in choices_data]
        return cls(
            id=data['id'],
            object=data['object'],
            created=data['created'],
            model=data['model'],
            choices=choices
        )

@dataclass
class Chat:
    id: str
    object: str
    created: int
    model: str
    choices: List[Choice]
    usage: Usage
    system_fingerprint: str

    @classmethod
    def from_dict(cls, data: dict) -> 'Chat':
        choices_data = data.get('choices', [])
        choices = [Choice.from_dict(choice_data) for choice_data in choices_data]
        return cls(
            id=data['id'],
            object=data['object'],
            created=data['created'],
            model=data['model'],
            choices=choices,
            usage=Usage(**data['usage']),
            system_fingerprint=data['system_fingerprint']
        )

@dataclass
class Embedding:
    data: List[Any]
    model: str
    obj: str
