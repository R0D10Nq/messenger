"""Схемы для реакций на сообщения."""

import uuid
from datetime import datetime

from pydantic import BaseModel, Field


class ReactionCreate(BaseModel):
    """Запрос на добавление реакции."""

    emoji: str = Field(..., min_length=1, max_length=32, description="Эмодзи реакции")


class ReactionResponse(BaseModel):
    """Ответ с реакцией."""

    id: uuid.UUID
    message_id: uuid.UUID
    user_id: uuid.UUID
    user_name: str
    emoji: str
    created_at: datetime

    model_config = {"from_attributes": True}


class ReactionSummary(BaseModel):
    """Сводка реакций на сообщение."""

    emoji: str
    count: int
    users: list[str]
    reacted_by_me: bool = False


class MessageReactionsResponse(BaseModel):
    """Ответ со всеми реакциями на сообщение."""

    message_id: uuid.UUID
    reactions: list[ReactionSummary]
    total_count: int
