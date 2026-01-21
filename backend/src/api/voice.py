"""API эндпоинты для голосовых сообщений."""

import uuid
from datetime import UTC, datetime, timedelta

from fastapi import APIRouter, Depends, HTTPException, UploadFile, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.deps import get_current_user
from src.db import get_db
from src.models.chat import Chat, ChatMember, Message
from src.models.user import User
from src.schemas.voice import (
    VoiceMessageCreate,
    VoiceMessageListenRequest,
    VoiceMessageResponse,
    VoiceTranscriptionResponse,
)

router = APIRouter(prefix="/voice", tags=["voice"])


async def check_chat_access(
    db: AsyncSession, user_id: uuid.UUID, chat_id: uuid.UUID
) -> Chat:
    """Проверяет доступ пользователя к чату."""
    chat = await db.get(Chat, chat_id)
    if not chat:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"message": "Чат не найден", "code": "chat_not_found"},
        )

    member_result = await db.execute(
        select(ChatMember)
        .where(ChatMember.chat_id == chat_id)
        .where(ChatMember.user_id == user_id)
    )
    if not member_result.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={"message": "Нет доступа к чату", "code": "no_access"},
        )

    return chat


@router.post("/upload", status_code=status.HTTP_201_CREATED)
async def upload_voice_message(
    file: UploadFile,
    chat_id: uuid.UUID,
    duration: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> dict:
    """Загрузить голосовое сообщение."""
    await check_chat_access(db, current_user.id, chat_id)

    if not file.content_type or not file.content_type.startswith("audio/"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"message": "Файл должен быть аудио", "code": "invalid_file_type"},
        )

    if duration < 1 or duration > 600:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"message": "Длительность должна быть от 1 до 600 секунд", "code": "invalid_duration"},
        )

    message = Message(
        chat_id=chat_id,
        sender_id=current_user.id,
        content="[Голосовое сообщение]",
        message_type="voice",
    )
    db.add(message)
    await db.flush()
    await db.refresh(message)

    return {
        "message_id": str(message.id),
        "chat_id": str(chat_id),
        "duration": duration,
        "created_at": message.created_at.isoformat(),
    }


@router.post("/{message_id}/listen", status_code=status.HTTP_204_NO_CONTENT)
async def mark_as_listened(
    message_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> None:
    """Отметить голосовое сообщение как прослушанное."""
    message = await db.get(Message, message_id)
    if not message:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"message": "Сообщение не найдено", "code": "message_not_found"},
        )

    await check_chat_access(db, current_user.id, message.chat_id)

    if message.sender_id == current_user.id:
        return

    message.is_read = True
    await db.flush()


@router.get("/{message_id}/transcribe")
async def transcribe_voice_message(
    message_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> VoiceTranscriptionResponse:
    """Получить транскрипцию голосового сообщения (заглушка)."""
    message = await db.get(Message, message_id)
    if not message:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"message": "Сообщение не найдено", "code": "message_not_found"},
        )

    await check_chat_access(db, current_user.id, message.chat_id)

    if message.message_type != "voice":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"message": "Сообщение не является голосовым", "code": "not_voice_message"},
        )

    return VoiceTranscriptionResponse(
        message_id=message_id,
        text="[Транскрипция недоступна]",
        language="ru",
        confidence=None,
    )


@router.get("/chat/{chat_id}")
async def get_voice_messages(
    chat_id: uuid.UUID,
    limit: int = 20,
    offset: int = 0,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> list[dict]:
    """Получить голосовые сообщения чата."""
    await check_chat_access(db, current_user.id, chat_id)

    result = await db.execute(
        select(Message)
        .where(Message.chat_id == chat_id)
        .where(Message.message_type == "voice")
        .order_by(Message.created_at.desc())
        .offset(offset)
        .limit(limit)
    )
    messages = result.scalars().all()

    return [
        {
            "id": str(m.id),
            "chat_id": str(m.chat_id),
            "sender_id": str(m.sender_id),
            "content": m.content,
            "is_read": m.is_read,
            "created_at": m.created_at.isoformat(),
        }
        for m in messages
    ]
