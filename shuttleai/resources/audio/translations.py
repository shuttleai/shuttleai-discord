from typing import Optional

from shuttleai.resources.common import AsyncResource, SyncResource
from shuttleai.schemas.audio.translations import AudioTranslationResponse


class AsyncTranslations(AsyncResource):
    async def create(
        self,
        file: str,
        model: Optional[str] = None,
    ) -> AudioTranslationResponse:
        request = self._client._make_audio_trans_request(
            file,
            model,
        )

        return await self.handle_request(  # type: ignore
            method="post",
            endpoint="v1/audio/translations",
            request_data=request,
            response_cls=AudioTranslationResponse,
        )


class SyncTranslations(SyncResource):
    def create(
        self,
        file: str,
        model: Optional[str] = None,
    ) -> AudioTranslationResponse:
        request = self._client._make_audio_trans_request(
            file,
            model,
        )

        return await self.handle_request(  # type: ignore
            method="post",
            endpoint="v1/audio/translations",
            request_data=request,
            response_cls=AudioTranslationResponse,
        )
