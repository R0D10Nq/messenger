"""Схемы для чатов и сообщений."""

import uuid
from datetime import datetime

from pydantic import BaseModel, Field


class CreateDirectChatRequest(BaseModel):
    """Запрос на создание прямого чата."""

    user_id: uuid.UUID


class CreateGroupChatRequest(BaseModel):
    """Запрос на создание группового чата."""

    name: str = Field(min_length=1, max_length=100)
    description: str | None = Field(None, max_length=500)
    member_ids: list[uuid.UUID] = Field(default_factory=list)


class UpdateGroupChatRequest(BaseModel):
    """Запрос на обновление группового чата."""

    name: str | None = Field(None, min_length=1, max_length=100)
    description: str | None = Field(None, max_length=500)
    avatar_url: str | None = Field(None, max_length=500)


class AddMembersRequest(BaseModel):
    """Запрос на добавление участников."""

    user_ids: list[uuid.UUID]


class UpdateMemberRoleRequest(BaseModel):
    """Запрос на изменение роли участника."""

    role: str = Field(pattern="^(admin|member)$")


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
    role: str
    joined_at: datetime


class ChatResponse(BaseModel):
    """Ответ с данными чата."""

    id: uuid.UUID
    chat_type: str
    name: str | None
    description: str | None
    avatar_url: str | None
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
