from .audio.audio import AsyncAudio, Audio
from .chat.completions import AsyncChat, Chat
from .embeddings import AsyncEmbeddings, Embeddings
from .etc.insults import AsyncInsults, Insults
from .etc.jokes import AsyncJokes, Jokes
from .images.generations import AsyncImages, Images
from .moderations import AsyncModerations, Moderations

__all__ = [
    "AsyncChat",
    "Chat",
    "AsyncImages",
    "Images",
    "AsyncAudio",
    "Audio",
    "AsyncModerations",
    "Moderations",
    "AsyncEmbeddings",
    "Embeddings",
    "AsyncInsults",
    "Insults",
    "AsyncJokes",
    "Jokes",
    # Add new resources here
]
