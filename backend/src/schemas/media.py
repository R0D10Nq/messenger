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
