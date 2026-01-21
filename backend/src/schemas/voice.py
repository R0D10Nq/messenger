"""Схемы для голосовых сообщений."""

import uuid
from datetime import datetime

from pydantic import BaseModel, Field


class VoiceMessageCreate(BaseModel):
    """Запрос на создание голосового сообщения."""

    chat_id: uuid.UUID
    duration: int = Field(..., ge=1, le=600, description="Длительность в секундах")
    waveform: list[int] | None = Field(None, description="Визуализация волны (0-100)")


class VoiceMessageResponse(BaseModel):
    """Ответ с голосовым сообщением."""

    id: uuid.UUID
    message_id: uuid.UUID
    chat_id: uuid.UUID
    sender_id: uuid.UUID
    file_url: str
    duration: int
    waveform: list[int] | None
    is_listened: bool
    created_at: datetime

    model_config = {"from_attributes": True}


class VoiceMessageUploadResponse(BaseModel):
    """Ответ после загрузки голосового сообщения."""

    upload_url: str
    voice_message_id: uuid.UUID
    expires_at: datetime


class VoiceMessageListenRequest(BaseModel):
    """Запрос на отметку прослушивания."""

    message_id: uuid.UUID


class VoiceTranscriptionResponse(BaseModel):
    """Ответ с транскрипцией голосового сообщения."""

    message_id: uuid.UUID
    text: str
    language: str | None
    confidence: float | None
