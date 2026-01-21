"""API эндпоинты для smart replies."""

import random
import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.deps import get_current_user
from src.db import get_db
from src.models.chat import Message
from src.models.user import User
from src.schemas.smart_reply import (
    QUICK_REPLIES,
    SmartReplyRequest,
    SmartReplyResponse,
    SmartReplySettingsRequest,
    SmartReplySettingsResponse,
)

router = APIRouter(prefix="/smart-reply", tags=["smart-reply"])

USER_SETTINGS: dict[str, dict] = {}


def classify_message(text: str) -> str:
    """Классифицирует тип сообщения для выбора ответов."""
    text_lower = text.lower()

    if any(word in text_lower for word in ["привет", "здравствуй", "добрый", "приветствую"]):
        return "greeting"

    if any(word in text_lower for word in ["спасибо", "благодар"]):
        return "thanks"

    if text.endswith("?"):
        return "question"

    if any(word in text_lower for word in ["пока", "до свидания", "прощай"]):
        return "farewell"

    if any(word in text_lower for word in ["хорошо", "ладно", "договорились", "окей"]):
        return "confirmation"

    return "agreement"


def generate_replies(message_text: str, max_count: int = 3) -> list[str]:
    """Генерирует варианты быстрых ответов."""
    category = classify_message(message_text)
    replies = QUICK_REPLIES.get(category, QUICK_REPLIES["agreement"])

    selected = random.sample(replies, min(len(replies), max_count))
    return selected


@router.post("/generate", response_model=SmartReplyResponse)
async def generate_smart_replies(
    request: SmartReplyRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> SmartReplyResponse:
    """Сгенерировать умные ответы на сообщение."""
    message = await db.get(Message, request.message_id)
    if not message:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"message": "Сообщение не найдено", "code": "message_not_found"},
        )

    settings = USER_SETTINGS.get(str(current_user.id), {"max_suggestions": 3})
    max_count = settings.get("max_suggestions", 3)

    replies = generate_replies(message.content, max_count)

    return SmartReplyResponse(
        replies=replies,
        confidence=[0.8, 0.7, 0.6][:len(replies)],
    )


@router.post("/quick", response_model=SmartReplyResponse)
async def get_quick_replies(
    text: str,
    current_user: User = Depends(get_current_user),
) -> SmartReplyResponse:
    """Быстрые ответы без сохранения в БД."""
    settings = USER_SETTINGS.get(str(current_user.id), {"max_suggestions": 3})
    max_count = settings.get("max_suggestions", 3)

    replies = generate_replies(text, max_count)

    return SmartReplyResponse(replies=replies)


@router.get("/settings", response_model=SmartReplySettingsResponse)
async def get_smart_reply_settings(
    current_user: User = Depends(get_current_user),
) -> SmartReplySettingsResponse:
    """Получить настройки smart replies."""
    settings = USER_SETTINGS.get(str(current_user.id), {
        "enabled": True,
        "max_suggestions": 3,
        "include_emoji": True,
        "formal_style": False,
    })

    return SmartReplySettingsResponse(**settings)


@router.put("/settings", response_model=SmartReplySettingsResponse)
async def update_smart_reply_settings(
    request: SmartReplySettingsRequest,
    current_user: User = Depends(get_current_user),
) -> SmartReplySettingsResponse:
    """Обновить настройки smart replies."""
    USER_SETTINGS[str(current_user.id)] = request.model_dump()

    return SmartReplySettingsResponse(**request.model_dump())
