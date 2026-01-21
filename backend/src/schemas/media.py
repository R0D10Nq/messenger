"""Схемы для медиафайлов."""

import uuid
from datetime import datetime

from pydantic import BaseModel


class MediaFileResponse(BaseModel):
    """Ответ с данными медиафайла."""

    id: uuid.UUID
    media_type: str
    filename: str
    original_filename: str
    mime_type: str
    file_size: int
    url: str
    thumbnail_url: str | None
    duration_seconds: int | None
    width: int | None
    height: int | None
    created_at: datetime

    model_config = {"from_attributes": True}


class AttachmentResponse(BaseModel):
    """Ответ с данными вложения."""

    id: uuid.UUID
    media: MediaFileResponse
    order: int


class UploadResponse(BaseModel):
    """Ответ на загрузку файла."""

    media: MediaFileResponse
    message: str


class TranscriptionResponse(BaseModel):
    """Ответ с данными транскрипции."""

    id: uuid.UUID
    media_id: uuid.UUID
    status: str
    text: str | None
    language: str | None
    duration_seconds: float | None
    error_message: str | None
    created_at: datetime
    completed_at: datetime | None

    model_config = {"from_attributes": True}


class CreateTranscriptionRequest(BaseModel):
    """Запрос на создание транскрипции."""

    media_id: uuid.UUID
