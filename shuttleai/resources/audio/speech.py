from typing import Optional

from shuttleai.resources.common import AsyncResource, SyncResource
from shuttleai.schemas.audio.speech import AudioSpeechResponse


class AsyncSpeech(AsyncResource):
    async def generate(
        self,
        input: str,
        model: str = "eleven-labs",
        voice: Optional[str] = None,
    ) -> AudioSpeechResponse:
        request = self._client._make_audio_speech_request(input, model, voice)

        return await self.handle_request(  # type: ignore
            method="post",
            endpoint="/audio/speech",
            request_data=request,
            response_cls=AudioSpeechResponse,
        )


class SyncSpeech(SyncResource):
    def generate(
        self,
        input: str,
        model: str = "eleven-labs",
        voice: Optional[str] = None,
    ) -> AudioSpeechResponse:
        request = self._client._make_audio_speech_request(input, model, voice)

        return self.handle_request(  # type: ignore
            method="post",
            endpoint="/audio/speech",
            request_data=request,
            response_cls=AudioSpeechResponse,
        )
