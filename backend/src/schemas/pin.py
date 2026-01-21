"""Схемы для закреплённых сообщений."""

import uuid
from datetime import datetime

from pydantic import BaseModel


class PinnedMessageResponse(BaseModel):
    """Ответ с закреплённым сообщением."""

    id: uuid.UUID
    chat_id: uuid.UUID
    message_id: uuid.UUID
    message_content: str
    pinned_by_id: uuid.UUID
    pinned_by_name: str
    pinned_at: datetime

    model_config = {"from_attributes": True}


class PinnedMessagesListResponse(BaseModel):
    """Список закреплённых сообщений."""

    chat_id: uuid.UUID
    pinned_messages: list[PinnedMessageResponse]
    count: int
