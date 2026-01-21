"""Схемы для 2FA [SECURITY]."""

from pydantic import BaseModel, Field


class Setup2FAResponse(BaseModel):
    """Ответ на запрос настройки 2FA."""

    secret: str
    provisioning_uri: str
    qr_code: str


class Verify2FARequest(BaseModel):
    """Запрос на подтверждение 2FA кода."""

    code: str = Field(min_length=6, max_length=6, pattern=r"^\d{6}$")


class Verify2FAResponse(BaseModel):
    """Ответ на подтверждение 2FA."""

    success: bool
    message: str


class TwoFactorStatusResponse(BaseModel):
    """Статус 2FA."""

    enabled: bool


class LoginWith2FARequest(BaseModel):
    """Запрос на логин с 2FA."""

    code: str = Field(min_length=6, max_length=6, pattern=r"^\d{6}$")
