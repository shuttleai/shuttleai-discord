from typing import Optional

from shuttleai.client.base import ClientBase
from shuttleai.resources.audio.speech import AsyncSpeech, SyncSpeech
from shuttleai.resources.audio.transcriptions import (
    AsyncTranscriptions,
    SyncTranscriptions,
)
from shuttleai.resources.audio.translations import AsyncTranslations, SyncTranslations


class Audio:
    def __init__(self, client: ClientBase):
        self._speech: Optional[SyncSpeech] = None
        self._transcriptions: Optional[SyncTranscriptions] = None
        self._translations: Optional[SyncTranslations] = None
        self._client = client

    @property
    def speech(self) -> SyncSpeech:
        if self._speech is None:
            self._speech = SyncSpeech(self._client)
        return self._speech

    @property
    def transcriptions(self) -> SyncTranscriptions:
        if self._transcriptions is None:
            self._transcriptions = SyncTranscriptions(self._client)
        return self._transcriptions

    @property
    def translations(self) -> SyncTranslations:
        if self._translations is None:
            self._translations = SyncTranslations(self._client)
        return self._translations


class AsyncAudio:
    def __init__(self, client: ClientBase):
        self._speech: Optional[AsyncSpeech] = None
        self._transcriptions: Optional[AsyncTranscriptions] = None
        self._translations: Optional[AsyncTranslations] = None
        self._client = client

    @property
    def speech(self) -> AsyncSpeech:
        if self._speech is None:
            self._speech = AsyncSpeech(self._client)
        return self._speech

    @property
    def transcriptions(self) -> AsyncTranscriptions:
        if self._transcriptions is None:
            self._transcriptions = AsyncTranscriptions(self._client)
        return self._transcriptions

    @property
    def translations(self) -> AsyncTranslations:
        if self._translations is None:
            self._translations = AsyncTranslations(self._client)
        return self._translations
