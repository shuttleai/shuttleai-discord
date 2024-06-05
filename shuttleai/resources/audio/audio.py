from functools import cached_property
from typing import Generic, Type, TypeVar

from shuttleai.client.base import ClientBase
from shuttleai.resources.audio.speech import AsyncSpeech, SyncSpeech
from shuttleai.resources.audio.transcriptions import (
    AsyncTranscriptions,
    SyncTranscriptions,
)
from shuttleai.resources.audio.translations import AsyncTranslations, SyncTranslations
from shuttleai.resources.common import T

SpeechType = TypeVar("SpeechType", SyncSpeech, AsyncSpeech)
TranscriptionsType = TypeVar("TranscriptionsType", SyncTranscriptions, AsyncTranscriptions)
TranslationsType = TypeVar("TranslationsType", SyncTranslations, AsyncTranslations)

class BaseAudio(Generic[T, SpeechType, TranscriptionsType, TranslationsType]):
    _client: T
    _speech_class: Type[SpeechType]
    _transcriptions_class: Type[TranscriptionsType]
    _translations_class: Type[TranslationsType]

    def __init__(
        self,
        client: T,
        speech_class: Type[SpeechType],
        transcriptions_class: Type[TranscriptionsType],
        translations_class: Type[TranslationsType]
    ) -> None:
        self._client = client
        self._speech_class = speech_class
        self._transcriptions_class = transcriptions_class
        self._translations_class = translations_class

    @cached_property
    def speech(self) -> SpeechType:
        return self._speech_class(self._client)

    @cached_property
    def transcriptions(self) -> TranscriptionsType:
        return self._transcriptions_class(self._client)

    @cached_property
    def translations(self) -> TranslationsType:
        return self._translations_class(self._client)


class Audio(BaseAudio[ClientBase, SyncSpeech, SyncTranscriptions, SyncTranslations]):
    def __init__(self, client: ClientBase) -> None:
        super().__init__(client, SyncSpeech, SyncTranscriptions, SyncTranslations)

class AsyncAudio(BaseAudio[ClientBase, AsyncSpeech, AsyncTranscriptions, AsyncTranslations]):
    def __init__(self, client: ClientBase) -> None:
        super().__init__(client, AsyncSpeech, AsyncTranscriptions, AsyncTranslations)
