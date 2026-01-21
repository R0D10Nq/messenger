"""Схемы для E2E шифрования [SECURITY]."""

import uuid
from datetime import datetime

from pydantic import BaseModel, Field


class RegisterKeysRequest(BaseModel):
    """Запрос на регистрацию ключей устройства."""

    device_id: str = Field(min_length=1, max_length=100)
    identity_key: str = Field(min_length=1)
    signed_prekey: str = Field(min_length=1)
    signed_prekey_signature: str = Field(min_length=1)
    one_time_prekeys: list[str] = Field(default_factory=list, max_length=100)


class PublicKeyResponse(BaseModel):
    """Ответ с публичными ключами пользователя."""

    id: uuid.UUID
    user_id: uuid.UUID
    device_id: str
    identity_key: str
    signed_prekey: str
    signed_prekey_signature: str
    created_at: datetime

    model_config = {"from_attributes": True}


class KeyBundleResponse(BaseModel):
    """Пакет ключей для установки сессии."""

    identity_key: str
    signed_prekey: str
    signed_prekey_signature: str
    one_time_prekey: str | None


class UploadPrekeysRequest(BaseModel):
    """Запрос на загрузку дополнительных prekeys."""

    prekeys: list[str] = Field(min_length=1, max_length=100)


class PrekeysCountResponse(BaseModel):
    """Количество доступных prekeys."""

    count: int
    device_id: str
