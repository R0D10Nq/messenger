"""Схемы для экспорта переписок."""

import uuid
from datetime import datetime
from enum import Enum

from pydantic import BaseModel, Field


class ExportFormat(str, Enum):
    """Формат экспорта."""

    JSON = "json"
    HTML = "html"
    TXT = "txt"


class ExportStatus(str, Enum):
    """Статус экспорта."""

    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"


class ExportChatRequest(BaseModel):
    """Запрос на экспорт чата."""

    chat_id: uuid.UUID
    format: ExportFormat = ExportFormat.JSON
    include_media: bool = True
    start_date: datetime | None = None
    end_date: datetime | None = None


class ExportJobResponse(BaseModel):
    """Ответ с информацией о задаче экспорта."""

    id: uuid.UUID
    chat_id: uuid.UUID
    user_id: uuid.UUID
    format: ExportFormat
    status: ExportStatus
    include_media: bool
    file_url: str | None
    file_size: int | None
    message_count: int | None
    error_message: str | None
    created_at: datetime
    completed_at: datetime | None

    model_config = {"from_attributes": True}


class ExportListResponse(BaseModel):
    """Список экспортов пользователя."""

    exports: list[ExportJobResponse]
    total: int


class ExportProgressResponse(BaseModel):
    """Прогресс экспорта."""

    job_id: uuid.UUID
    status: ExportStatus
    progress: int = Field(..., ge=0, le=100)
    message_count: int | None
    current_message: int | None


class ExportedMessage(BaseModel):
    """Экспортированное сообщение."""

    id: uuid.UUID
    sender_id: uuid.UUID
    sender_name: str
    content: str
    message_type: str
    created_at: datetime
    edited_at: datetime | None
    attachments: list[dict] | None
    reactions: list[dict] | None


class ExportedChat(BaseModel):
    """Экспортированный чат."""

    id: uuid.UUID
    name: str
    chat_type: str
    created_at: datetime
    exported_at: datetime
    message_count: int
    participants: list[dict]
    messages: list[ExportedMessage]
