"""Схемы для мульти-устройств."""

import uuid
from datetime import datetime
from enum import Enum

from pydantic import BaseModel, Field


class DeviceType(str, Enum):
    """Тип устройства."""

    DESKTOP = "desktop"
    MOBILE = "mobile"
    TABLET = "tablet"
    WEB = "web"
    UNKNOWN = "unknown"


class DevicePlatform(str, Enum):
    """Платформа устройства."""

    WINDOWS = "windows"
    MACOS = "macos"
    LINUX = "linux"
    ANDROID = "android"
    IOS = "ios"
    WEB = "web"
    UNKNOWN = "unknown"


class DeviceRegisterRequest(BaseModel):
    """Запрос на регистрацию устройства."""

    device_name: str = Field(..., min_length=1, max_length=100)
    device_type: DeviceType = DeviceType.UNKNOWN
    platform: DevicePlatform = DevicePlatform.UNKNOWN
    push_token: str | None = None


class DeviceResponse(BaseModel):
    """Ответ с информацией об устройстве."""

    id: uuid.UUID
    user_id: uuid.UUID
    device_name: str
    device_type: DeviceType
    platform: DevicePlatform
    is_current: bool
    last_active_at: datetime
    ip_address: str | None
    location: str | None
    created_at: datetime

    model_config = {"from_attributes": True}


class DeviceListResponse(BaseModel):
    """Список устройств пользователя."""

    devices: list[DeviceResponse]
    current_device_id: uuid.UUID | None


class DeviceUpdateRequest(BaseModel):
    """Запрос на обновление устройства."""

    device_name: str | None = None
    push_token: str | None = None


class SessionResponse(BaseModel):
    """Информация о сессии."""

    device_id: uuid.UUID
    device_name: str
    device_type: DeviceType
    platform: DevicePlatform
    is_current: bool
    last_active_at: datetime
    ip_address: str | None
    location: str | None


class TerminateSessionsRequest(BaseModel):
    """Запрос на завершение сессий."""

    device_ids: list[uuid.UUID] | None = None
    terminate_all_except_current: bool = False
