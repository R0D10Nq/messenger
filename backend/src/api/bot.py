"""API эндпоинты для ботов."""

import secrets
import uuid
from datetime import UTC, datetime

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.deps import get_current_user
from src.db import get_db
from src.models.user import User
from src.schemas.bot import (
    BotCommand,
    BotCommandsRequest,
    BotMessageRequest,
    BotMessageResponse,
    BotResponse,
    BotStatus,
    BotUpdateRequest,
    CreateBotRequest,
    WebhookConfig,
)

router = APIRouter(prefix="/bots", tags=["bots"])

BOTS: dict[str, dict] = {}
BOT_COMMANDS: dict[str, list[BotCommand]] = {}
BOT_WEBHOOKS: dict[str, WebhookConfig] = {}


def generate_api_token() -> str:
    """Генерирует API токен для бота."""
    return secrets.token_urlsafe(32)


@router.post("", response_model=BotResponse)
async def create_bot(
    request: CreateBotRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> BotResponse:
    """Создать нового бота."""
    for bot in BOTS.values():
        if bot["username"] == request.username:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail={"message": "Имя пользователя занято", "code": "username_taken"},
            )

    bot_id = uuid.uuid4()
    now = datetime.now(UTC)
    api_token = generate_api_token()

    bot = {
        "id": bot_id,
        "name": request.name,
        "username": request.username,
        "description": request.description,
        "about": request.about,
        "owner_id": current_user.id,
        "status": BotStatus.ACTIVE,
        "api_token": api_token,
        "created_at": now,
    }

    BOTS[str(bot_id)] = bot
    BOT_COMMANDS[str(bot_id)] = []

    return BotResponse(**bot)


@router.get("", response_model=list[BotResponse])
async def list_my_bots(
    current_user: User = Depends(get_current_user),
) -> list[BotResponse]:
    """Получить список своих ботов."""
    user_bots = [
        BotResponse(**bot)
        for bot in BOTS.values()
        if bot["owner_id"] == current_user.id
    ]
    return user_bots


@router.get("/{bot_id}", response_model=BotResponse)
async def get_bot(
    bot_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
) -> BotResponse:
    """Получить информацию о боте."""
    bot = BOTS.get(str(bot_id))
    if not bot:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"message": "Бот не найден", "code": "bot_not_found"},
        )

    response_bot = {**bot}
    if bot["owner_id"] != current_user.id:
        response_bot["api_token"] = None

    return BotResponse(**response_bot)


@router.put("/{bot_id}", response_model=BotResponse)
async def update_bot(
    bot_id: uuid.UUID,
    request: BotUpdateRequest,
    current_user: User = Depends(get_current_user),
) -> BotResponse:
    """Обновить бота."""
    bot = BOTS.get(str(bot_id))
    if not bot:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"message": "Бот не найден", "code": "bot_not_found"},
        )

    if bot["owner_id"] != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={"message": "Нет прав", "code": "no_permission"},
        )

    if request.name is not None:
        bot["name"] = request.name
    if request.description is not None:
        bot["description"] = request.description
    if request.about is not None:
        bot["about"] = request.about

    return BotResponse(**bot)


@router.delete("/{bot_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_bot(
    bot_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
) -> None:
    """Удалить бота."""
    bot = BOTS.get(str(bot_id))
    if not bot:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"message": "Бот не найден", "code": "bot_not_found"},
        )

    if bot["owner_id"] != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={"message": "Нет прав", "code": "no_permission"},
        )

    del BOTS[str(bot_id)]
    BOT_COMMANDS.pop(str(bot_id), None)
    BOT_WEBHOOKS.pop(str(bot_id), None)


@router.post("/{bot_id}/token", response_model=dict)
async def regenerate_token(
    bot_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
) -> dict:
    """Перегенерировать API токен бота."""
    bot = BOTS.get(str(bot_id))
    if not bot or bot["owner_id"] != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"message": "Бот не найден", "code": "bot_not_found"},
        )

    new_token = generate_api_token()
    bot["api_token"] = new_token

    return {"api_token": new_token}


@router.post("/{bot_id}/commands", response_model=list[BotCommand])
async def set_commands(
    bot_id: uuid.UUID,
    request: BotCommandsRequest,
    current_user: User = Depends(get_current_user),
) -> list[BotCommand]:
    """Установить команды бота."""
    bot = BOTS.get(str(bot_id))
    if not bot or bot["owner_id"] != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"message": "Бот не найден", "code": "bot_not_found"},
        )

    BOT_COMMANDS[str(bot_id)] = request.commands
    return request.commands


@router.get("/{bot_id}/commands", response_model=list[BotCommand])
async def get_commands(
    bot_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
) -> list[BotCommand]:
    """Получить команды бота."""
    if str(bot_id) not in BOTS:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"message": "Бот не найден", "code": "bot_not_found"},
        )

    return BOT_COMMANDS.get(str(bot_id), [])


@router.post("/{bot_id}/message", response_model=BotMessageResponse)
async def send_message(
    bot_id: uuid.UUID,
    request: BotMessageRequest,
    current_user: User = Depends(get_current_user),
) -> BotMessageResponse:
    """Отправить сообщение от имени бота."""
    bot = BOTS.get(str(bot_id))
    if not bot or bot["owner_id"] != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"message": "Бот не найден", "code": "bot_not_found"},
        )

    message_id = uuid.uuid4()
    now = datetime.now(UTC)

    return BotMessageResponse(
        message_id=message_id,
        chat_id=request.chat_id,
        sent_at=now,
    )


@router.post("/{bot_id}/webhook")
async def set_webhook(
    bot_id: uuid.UUID,
    config: WebhookConfig,
    current_user: User = Depends(get_current_user),
) -> dict:
    """Установить вебхук для бота."""
    bot = BOTS.get(str(bot_id))
    if not bot or bot["owner_id"] != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"message": "Бот не найден", "code": "bot_not_found"},
        )

    BOT_WEBHOOKS[str(bot_id)] = config

    return {"success": True, "url": config.url}


@router.delete("/{bot_id}/webhook")
async def delete_webhook(
    bot_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
) -> dict:
    """Удалить вебхук бота."""
    bot = BOTS.get(str(bot_id))
    if not bot or bot["owner_id"] != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"message": "Бот не найден", "code": "bot_not_found"},
        )

    BOT_WEBHOOKS.pop(str(bot_id), None)

    return {"success": True}
