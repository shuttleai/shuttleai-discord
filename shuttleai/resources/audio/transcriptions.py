from typing import Optional

from shuttleai.resources._resource import AsyncResource, SyncResource
from shuttleai.schemas.audio.transcriptions import AudioTranscriptionResponse


class AsyncTranscriptions(AsyncResource):
    async def create(
        self,
        file: str,
        model: Optional[str] = None,
    ) -> AudioTranscriptionResponse:
        request = self._client._make_audio_trans_request(
            file,
            model,
        )

        return await self.handle_request(  # type: ignore
            method="post",
            endpoint="v1/audio/transcriptions",
            request_data=request,
            response_cls=AudioTranscriptionResponse,
        )


class SyncTranscriptions(SyncResource):
    def create(
        self,
        file: str,
        model: Optional[str] = None,
    ) -> AudioTranscriptionResponse:
        request = self._client._make_audio_trans_request(
            file,
            model,
        )

        return await self.handle_request(  # type: ignore
            method="post",
            endpoint="v1/audio/transcriptions",
            request_data=request,
            response_cls=AudioTranscriptionResponse,
        )
