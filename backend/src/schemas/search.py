"""Схемы для поиска."""

import uuid
from datetime import datetime
from enum import Enum

from pydantic import BaseModel, Field


class SearchType(str, Enum):
    """Тип поиска."""

    ALL = "all"
    TEXT = "text"
    MEDIA = "media"
    VOICE = "voice"


class SearchRequest(BaseModel):
    """Запрос на поиск."""

    query: str = Field(..., min_length=1, max_length=500, description="Поисковый запрос")
    chat_id: uuid.UUID | None = Field(None, description="ID чата для поиска")
    search_type: SearchType = Field(SearchType.ALL, description="Тип поиска")
    sender_id: uuid.UUID | None = Field(None, description="ID отправителя")
    date_from: datetime | None = Field(None, description="Дата начала")
    date_to: datetime | None = Field(None, description="Дата окончания")
    limit: int = Field(20, ge=1, le=100, description="Лимит результатов")
    offset: int = Field(0, ge=0, description="Смещение")


class SearchResultItem(BaseModel):
    """Элемент результата поиска."""

    message_id: uuid.UUID
    chat_id: uuid.UUID
    chat_name: str
    sender_id: uuid.UUID
    sender_name: str
    content: str
    highlight: str
    created_at: datetime
    has_media: bool = False


class SearchResponse(BaseModel):
    """Ответ на поиск."""

    query: str
    total_count: int
    results: list[SearchResultItem]
    has_more: bool
