"""Схемы для чатов и сообщений."""

import uuid
from datetime import datetime

from pydantic import BaseModel, Field


class CreateDirectChatRequest(BaseModel):
    """Запрос на создание прямого чата."""

    user_id: uuid.UUID


class SendMessageRequest(BaseModel):
    """Запрос на отправку сообщения."""

    content: str = Field(min_length=1, max_length=10000)
    reply_to_id: uuid.UUID | None = None


class EditMessageRequest(BaseModel):
    """Запрос на редактирование сообщения."""

    content: str = Field(min_length=1, max_length=10000)


class MessageResponse(BaseModel):
    """Ответ с данными сообщения."""

    id: uuid.UUID
    chat_id: uuid.UUID
    sender_id: uuid.UUID
    sender_name: str
    content: str
    status: str
    reply_to_id: uuid.UUID | None
    edited_at: datetime | None
    created_at: datetime

    model_config = {"from_attributes": True}


class ChatMemberResponse(BaseModel):
    """Данные участника чата."""

    user_id: uuid.UUID
    name: str
    avatar_url: str | None
    joined_at: datetime


class ChatResponse(BaseModel):
    """Ответ с данными чата."""

    id: uuid.UUID
    chat_type: str
    name: str | None
    members: list[ChatMemberResponse]
    last_message: MessageResponse | None
    unread_count: int
    created_at: datetime

    model_config = {"from_attributes": True}


class ChatListResponse(BaseModel):
    """Список чатов."""

    chats: list[ChatResponse]
    total: int


class MessageListResponse(BaseModel):
    """Список сообщений."""

    messages: list[MessageResponse]
    total: int
    has_more: bool
