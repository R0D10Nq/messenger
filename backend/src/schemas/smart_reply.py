"""Схемы для smart replies."""

import uuid

from pydantic import BaseModel, Field


class SmartReplyRequest(BaseModel):
    """Запрос на генерацию умных ответов."""

    message_id: uuid.UUID
    context_messages: int = Field(5, ge=1, le=20)


class SmartReplyResponse(BaseModel):
    """Ответ с вариантами умных ответов."""

    replies: list[str]
    confidence: list[float] | None = None


class SmartReplySettingsRequest(BaseModel):
    """Настройки smart replies."""

    enabled: bool = True
    max_suggestions: int = Field(3, ge=1, le=5)
    include_emoji: bool = True
    formal_style: bool = False


class SmartReplySettingsResponse(BaseModel):
    """Текущие настройки smart replies."""

    enabled: bool
    max_suggestions: int
    include_emoji: bool
    formal_style: bool


QUICK_REPLIES = {
    "greeting": [
        "Привет!",
        "Здравствуй!",
        "Добрый день!",
    ],
    "thanks": [
        "Спасибо!",
        "Благодарю!",
        "Отлично, спасибо!",
    ],
    "agreement": [
        "Хорошо",
        "Договорились",
        "Отлично!",
    ],
    "question": [
        "Да",
        "Нет",
        "Возможно",
    ],
    "farewell": [
        "Пока!",
        "До свидания!",
        "До связи!",
    ],
    "confirmation": [
        "Понял",
        "Принято",
        "Ок, сделаю",
    ],
}
