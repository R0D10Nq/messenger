"""Схемы для профиля и контактов."""

import uuid
from datetime import datetime

from pydantic import BaseModel, Field


class ProfileUpdateRequest(BaseModel):
    """Запрос на обновление профиля."""

    name: str | None = Field(None, min_length=1, max_length=100)
    avatar_url: str | None = Field(None, max_length=500)
    status_message: str | None = Field(None, max_length=200)


class ContactCreateRequest(BaseModel):
    """Запрос на добавление контакта."""

    contact_id: uuid.UUID
    nickname: str | None = Field(None, max_length=100)


class ContactUpdateRequest(BaseModel):
    """Запрос на обновление контакта."""

    nickname: str | None = Field(None, max_length=100)


class ContactResponse(BaseModel):
    """Ответ с данными контакта."""

    id: uuid.UUID
    contact_id: uuid.UUID
    nickname: str | None
    status: str
    contact_name: str
    contact_email: str
    contact_avatar_url: str | None
    contact_status_message: str | None
    created_at: datetime

    model_config = {"from_attributes": True}


class ContactListResponse(BaseModel):
    """Список контактов."""

    contacts: list[ContactResponse]
    total: int
