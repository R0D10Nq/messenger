"""Схемы для каналов."""

import uuid
from datetime import datetime
from enum import Enum

from pydantic import BaseModel, Field


class ChannelType(str, Enum):
    """Тип канала."""

    PUBLIC = "public"
    PRIVATE = "private"


class ChannelRole(str, Enum):
    """Роль в канале."""

    OWNER = "owner"
    ADMIN = "admin"
    MODERATOR = "moderator"
    SUBSCRIBER = "subscriber"


class CreateChannelRequest(BaseModel):
    """Запрос на создание канала."""

    name: str = Field(..., min_length=1, max_length=100)
    username: str = Field(..., min_length=3, max_length=32, pattern=r"^[a-zA-Z0-9_]+$")
    description: str | None = Field(None, max_length=500)
    channel_type: ChannelType = ChannelType.PUBLIC
    allow_comments: bool = True


class ChannelResponse(BaseModel):
    """Ответ с информацией о канале."""

    id: uuid.UUID
    name: str
    username: str
    description: str | None
    channel_type: ChannelType
    owner_id: uuid.UUID
    subscriber_count: int
    allow_comments: bool
    created_at: datetime

    model_config = {"from_attributes": True}


class ChannelUpdateRequest(BaseModel):
    """Запрос на обновление канала."""

    name: str | None = None
    description: str | None = None
    allow_comments: bool | None = None


class ChannelStatsResponse(BaseModel):
    """Статистика канала."""

    subscriber_count: int
    total_posts: int
    total_views: int
    avg_views_per_post: float
    growth_rate: float
    top_posts: list[dict]


class ChannelPostRequest(BaseModel):
    """Запрос на публикацию в канале."""

    content: str = Field(..., min_length=1, max_length=4000)
    silent: bool = False
    schedule_at: datetime | None = None
    pin: bool = False


class ChannelPostResponse(BaseModel):
    """Ответ с информацией о публикации."""

    id: uuid.UUID
    channel_id: uuid.UUID
    content: str
    author_id: uuid.UUID
    views: int
    is_pinned: bool
    created_at: datetime

    model_config = {"from_attributes": True}


class ChannelMemberResponse(BaseModel):
    """Информация об участнике канала."""

    user_id: uuid.UUID
    username: str
    role: ChannelRole
    joined_at: datetime


class ScheduledPostResponse(BaseModel):
    """Запланированная публикация."""

    id: uuid.UUID
    content: str
    schedule_at: datetime
    created_at: datetime
