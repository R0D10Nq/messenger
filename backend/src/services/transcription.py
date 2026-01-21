"""Сервис транскрипции голосовых сообщений."""

import uuid
from datetime import UTC, datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.media import MediaFile, MediaType, Transcription, TranscriptionStatus


class TranscriptionService:
    """Сервис для транскрипции голосовых сообщений."""

    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def create_transcription(self, media_id: uuid.UUID) -> Transcription:
        """Создать задачу транскрипции для голосового сообщения."""
        media = await self.db.get(MediaFile, media_id)
        if not media:
            raise ValueError("Медиафайл не найден")

        if media.media_type != MediaType.VOICE.value:
            raise ValueError("Транскрипция доступна только для голосовых сообщений")

        existing = await self.db.execute(
            select(Transcription).where(Transcription.media_id == media_id)
        )
        if existing.scalar_one_or_none():
            raise ValueError("Транскрипция уже существует")

        transcription = Transcription(
            media_id=media_id,
            status=TranscriptionStatus.PENDING.value,
            duration_seconds=media.duration_seconds,
        )
        self.db.add(transcription)
        await self.db.flush()
        await self.db.refresh(transcription)

        return transcription

    async def get_transcription(self, media_id: uuid.UUID) -> Transcription | None:
        """Получить транскрипцию по ID медиафайла."""
        result = await self.db.execute(
            select(Transcription).where(Transcription.media_id == media_id)
        )
        return result.scalar_one_or_none()

    async def get_transcription_by_id(
        self, transcription_id: uuid.UUID
    ) -> Transcription | None:
        """Получить транскрипцию по её ID."""
        return await self.db.get(Transcription, transcription_id)

    async def update_status(
        self,
        transcription_id: uuid.UUID,
        status: TranscriptionStatus,
        text: str | None = None,
        language: str | None = None,
        error_message: str | None = None,
    ) -> Transcription | None:
        """Обновить статус транскрипции."""
        transcription = await self.db.get(Transcription, transcription_id)
        if not transcription:
            return None

        transcription.status = status.value

        if status == TranscriptionStatus.COMPLETED:
            transcription.text = text
            transcription.language = language
            transcription.completed_at = datetime.now(UTC)
        elif status == TranscriptionStatus.FAILED:
            transcription.error_message = error_message
            transcription.completed_at = datetime.now(UTC)

        await self.db.flush()
        await self.db.refresh(transcription)

        return transcription

    async def process_transcription(
        self,
        transcription_id: uuid.UUID,
    ) -> Transcription | None:
        """Обработать транскрипцию (заглушка для интеграции с STT).

        В реальной реализации здесь будет вызов внешнего STT сервиса
        (например, Whisper, Google Speech-to-Text, etc.)
        """
        transcription = await self.db.get(Transcription, transcription_id)
        if not transcription:
            return None

        await self.update_status(
            transcription_id,
            TranscriptionStatus.PROCESSING,
        )

        # TODO: Здесь будет интеграция с STT сервисом
        # Пример заглушки для демонстрации:
        # - Получить аудиофайл по media_id
        # - Отправить на STT сервис
        # - Получить результат и обновить статус

        return transcription
