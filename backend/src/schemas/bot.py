"""Схемы для ботов."""

import uuid
from datetime import datetime
from enum import Enum

from pydantic import BaseModel, Field


class BotStatus(str, Enum):
    """Статус бота."""

    ACTIVE = "active"
    INACTIVE = "inactive"
    SUSPENDED = "suspended"


class CommandType(str, Enum):
    """Тип команды бота."""

    TEXT = "text"
    BUTTON = "button"
    INLINE = "inline"


class CreateBotRequest(BaseModel):
    """Запрос на создание бота."""

    name: str = Field(..., min_length=1, max_length=64)
    username: str = Field(..., min_length=3, max_length=32, pattern=r"^[a-zA-Z0-9_]+$")
    description: str | None = Field(None, max_length=500)
    about: str | None = Field(None, max_length=200)


class BotResponse(BaseModel):
    """Ответ с информацией о боте."""

    id: uuid.UUID
    name: str
    username: str
    description: str | None
    about: str | None
    owner_id: uuid.UUID
    status: BotStatus
    api_token: str | None
    created_at: datetime

    model_config = {"from_attributes": True}


class BotCommand(BaseModel):
    """Команда бота."""

    command: str = Field(..., pattern=r"^[a-z0-9_]+$", max_length=32)
    description: str = Field(..., max_length=256)


class BotCommandsRequest(BaseModel):
    """Запрос на установку команд бота."""

    commands: list[BotCommand]


class BotButton(BaseModel):
    """Кнопка бота."""

    text: str = Field(..., max_length=64)
    callback_data: str | None = Field(None, max_length=64)
    url: str | None = None


class BotKeyboard(BaseModel):
    """Клавиатура бота."""

    buttons: list[list[BotButton]]
    resize: bool = True
    one_time: bool = False


class InlineButton(BaseModel):
    """Инлайн-кнопка."""

    text: str = Field(..., max_length=64)
    callback_data: str | None = None
    url: str | None = None
    switch_inline: str | None = None


class InlineKeyboard(BaseModel):
    """Инлайн-клавиатура."""

    buttons: list[list[InlineButton]]


class BotMessageRequest(BaseModel):
    """Запрос на отправку сообщения от бота."""

    chat_id: uuid.UUID
    text: str = Field(..., max_length=4000)
    keyboard: BotKeyboard | None = None
    inline_keyboard: InlineKeyboard | None = None
    reply_to_message_id: uuid.UUID | None = None


class BotMessageResponse(BaseModel):
    """Ответ после отправки сообщения."""

    message_id: uuid.UUID
    chat_id: uuid.UUID
    sent_at: datetime


class WebhookConfig(BaseModel):
    """Конфигурация вебхука."""

    url: str
    secret: str | None = None
    allowed_updates: list[str] | None = None


class BotUpdateRequest(BaseModel):
    """Запрос на обновление бота."""

    name: str | None = None
    description: str | None = None
    about: str | None = None
