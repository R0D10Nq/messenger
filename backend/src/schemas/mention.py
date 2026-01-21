"""Схемы для упоминаний и превью ссылок."""

import uuid

from pydantic import BaseModel, Field


class MentionData(BaseModel):
    """Данные об упоминании пользователя."""

    user_id: uuid.UUID
    user_name: str
    offset: int = Field(..., ge=0, description="Позиция начала в тексте")
    length: int = Field(..., ge=1, description="Длина упоминания")


class LinkPreview(BaseModel):
    """Превью ссылки."""

    url: str
    title: str | None = None
    description: str | None = None
    image_url: str | None = None
    site_name: str | None = None


class MessageWithMentions(BaseModel):
    """Сообщение с упоминаниями."""

    content: str
    mentions: list[MentionData] = Field(default_factory=list)
    link_previews: list[LinkPreview] = Field(default_factory=list)


class ParsedMessage(BaseModel):
    """Результат парсинга сообщения."""

    content: str
    mentions: list[MentionData]
    urls: list[str]
