"""Схемы для приглашений и превью."""

import uuid
from datetime import datetime
from enum import Enum

from pydantic import BaseModel, Field


class InviteType(str, Enum):
    """Тип приглашения."""

    CHAT = "chat"
    GROUP = "group"
    CHANNEL = "channel"


class InviteVisibility(str, Enum):
    """Видимость превью."""

    NONE = "none"
    BASIC = "basic"
    MESSAGES = "messages"


class CreateInviteRequest(BaseModel):
    """Запрос на создание приглашения."""

    chat_id: uuid.UUID
    expires_in_hours: int | None = Field(None, ge=1, le=720)
    max_uses: int | None = Field(None, ge=1, le=1000)
    preview_visibility: InviteVisibility = InviteVisibility.BASIC
    preview_message_count: int = Field(5, ge=0, le=20)


class InviteResponse(BaseModel):
    """Ответ с информацией о приглашении."""

    id: uuid.UUID
    code: str
    chat_id: uuid.UUID
    invite_type: InviteType
    created_by: uuid.UUID
    expires_at: datetime | None
    max_uses: int | None
    use_count: int
    preview_visibility: InviteVisibility
    is_active: bool
    created_at: datetime

    model_config = {"from_attributes": True}


class InvitePreviewResponse(BaseModel):
    """Превью приглашения для неавторизованных пользователей."""

    code: str
    chat_name: str
    chat_type: InviteType
    member_count: int
    avatar_url: str | None
    description: str | None
    preview_messages: list[dict] | None
    is_expired: bool
    requires_approval: bool


class InviteJoinRequest(BaseModel):
    """Запрос на присоединение по приглашению."""

    code: str


class InviteJoinResponse(BaseModel):
    """Ответ после присоединения."""

    success: bool
    chat_id: uuid.UUID
    message: str


class InviteListResponse(BaseModel):
    """Список приглашений чата."""

    invites: list[InviteResponse]
    total: int


class InviteRevokeRequest(BaseModel):
    """Запрос на отзыв приглашения."""

    invite_id: uuid.UUID
