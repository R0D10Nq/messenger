"""Схемы для аутентификации."""

import uuid
from datetime import datetime

from pydantic import BaseModel, EmailStr, Field


class RegisterRequest(BaseModel):
    """Запрос на регистрацию."""

    email: EmailStr
    password: str = Field(min_length=8, max_length=100)
    name: str = Field(min_length=1, max_length=100)


class LoginRequest(BaseModel):
    """Запрос на вход."""

    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    """Ответ с токенами."""

    access_token: str
    refresh_token: str
    token_type: str = "bearer"  # noqa: S105


class RefreshTokenRequest(BaseModel):
    """Запрос на обновление токена."""

    refresh_token: str


class UserResponse(BaseModel):
    """Данные пользователя."""

    id: uuid.UUID
    email: str
    name: str
    avatar_url: str | None = None
    status_message: str | None = None
    is_verified: bool
    created_at: datetime

    model_config = {"from_attributes": True}


class SessionResponse(BaseModel):
    """Данные сессии."""

    id: uuid.UUID
    device_info: str | None
    ip_address: str | None
    last_used_at: datetime
    created_at: datetime

    model_config = {"from_attributes": True}
