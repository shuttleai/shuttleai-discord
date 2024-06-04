from typing import Optional

from shuttleai.resources._resource import AsyncResource, SyncResource
from shuttleai.schemas.audio.speech import AudioSpeechResponse


class AsyncSpeech(AsyncResource):
    async def generate(
        self,
        prompt: str,
        model: Optional[str] = None,
    ) -> AudioSpeechResponse:
        request = self._client._make_audio_speech_request(
            prompt,
            model,
        )

        return await self.handle_request(  # type: ignore
            method="post",
            endpoint="v1/audio/speech",
            request_data=request,
            response_cls=AudioSpeechResponse,
        )


class SyncSpeech(SyncResource):
    def generate(
        self,
        prompt: str,
        model: Optional[str] = None,
    ) -> AudioSpeechResponse:
        request = self._client._make_audio_speech_request(
            prompt,
            model,
        )

        return self.handle_request(  # type: ignore
            method="post",
            endpoint="v1/audio/speech",
            request_data=request,
            response_cls=AudioSpeechResponse,
        )
