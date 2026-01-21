"""API эндпоинты для приглашений и превью."""

import secrets
import uuid
from datetime import UTC, datetime, timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.deps import get_current_user
from src.db import get_db
from src.models.chat import Chat, ChatMember
from src.models.user import User
from src.schemas.invite import (
    CreateInviteRequest,
    InviteJoinRequest,
    InviteJoinResponse,
    InviteListResponse,
    InvitePreviewResponse,
    InviteResponse,
    InviteType,
    InviteVisibility,
)

router = APIRouter(prefix="/invites", tags=["invites"])

INVITES: dict[str, dict] = {}


def generate_invite_code() -> str:
    """Генерирует уникальный код приглашения."""
    return secrets.token_urlsafe(8)


@router.post("", response_model=InviteResponse)
async def create_invite(
    request: CreateInviteRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> InviteResponse:
    """Создать приглашение в чат."""
    chat = await db.get(Chat, request.chat_id)
    if not chat:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"message": "Чат не найден", "code": "chat_not_found"},
        )

    member_result = await db.execute(
        select(ChatMember)
        .where(ChatMember.chat_id == request.chat_id)
        .where(ChatMember.user_id == current_user.id)
    )
    member = member_result.scalar_one_or_none()
    if not member or member.role not in ["owner", "admin"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={"message": "Нет прав для создания приглашения", "code": "no_permission"},
        )

    invite_id = uuid.uuid4()
    code = generate_invite_code()
    now = datetime.now(UTC)

    expires_at = None
    if request.expires_in_hours:
        expires_at = now + timedelta(hours=request.expires_in_hours)

    invite = {
        "id": invite_id,
        "code": code,
        "chat_id": request.chat_id,
        "invite_type": InviteType.GROUP if chat.is_group else InviteType.CHAT,
        "created_by": current_user.id,
        "expires_at": expires_at,
        "max_uses": request.max_uses,
        "use_count": 0,
        "preview_visibility": request.preview_visibility,
        "preview_message_count": request.preview_message_count,
        "is_active": True,
        "created_at": now,
    }

    INVITES[code] = invite

    return InviteResponse(**invite)


@router.get("/preview/{code}", response_model=InvitePreviewResponse)
async def get_invite_preview(
    code: str,
    db: AsyncSession = Depends(get_db),
) -> InvitePreviewResponse:
    """Получить превью приглашения (без авторизации)."""
    invite = INVITES.get(code)
    if not invite:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"message": "Приглашение не найдено", "code": "invite_not_found"},
        )

    is_expired = False
    if invite["expires_at"] and invite["expires_at"] < datetime.now(UTC):
        is_expired = True

    if invite["max_uses"] and invite["use_count"] >= invite["max_uses"]:
        is_expired = True

    chat = await db.get(Chat, invite["chat_id"])
    if not chat:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"message": "Чат не найден", "code": "chat_not_found"},
        )

    member_count_result = await db.execute(
        select(func.count(ChatMember.id)).where(ChatMember.chat_id == invite["chat_id"])
    )
    member_count = member_count_result.scalar() or 0

    preview_messages = None
    if invite["preview_visibility"] == InviteVisibility.MESSAGES:
        preview_messages = [
            {"content": "Пример сообщения 1", "sender": "Участник"},
            {"content": "Пример сообщения 2", "sender": "Другой участник"},
        ]

    return InvitePreviewResponse(
        code=code,
        chat_name=chat.name or "Чат",
        chat_type=invite["invite_type"],
        member_count=member_count,
        avatar_url=None,
        description=getattr(chat, "description", None),
        preview_messages=preview_messages,
        is_expired=is_expired,
        requires_approval=False,
    )


@router.post("/join", response_model=InviteJoinResponse)
async def join_by_invite(
    request: InviteJoinRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> InviteJoinResponse:
    """Присоединиться к чату по приглашению."""
    invite = INVITES.get(request.code)
    if not invite or not invite["is_active"]:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"message": "Приглашение не найдено или неактивно", "code": "invite_not_found"},
        )

    if invite["expires_at"] and invite["expires_at"] < datetime.now(UTC):
        raise HTTPException(
            status_code=status.HTTP_410_GONE,
            detail={"message": "Приглашение истекло", "code": "invite_expired"},
        )

    if invite["max_uses"] and invite["use_count"] >= invite["max_uses"]:
        raise HTTPException(
            status_code=status.HTTP_410_GONE,
            detail={"message": "Лимит использований исчерпан", "code": "invite_exhausted"},
        )

    existing_member = await db.execute(
        select(ChatMember)
        .where(ChatMember.chat_id == invite["chat_id"])
        .where(ChatMember.user_id == current_user.id)
    )
    if existing_member.scalar_one_or_none():
        return InviteJoinResponse(
            success=True,
            chat_id=invite["chat_id"],
            message="Вы уже являетесь участником этого чата",
        )

    new_member = ChatMember(
        chat_id=invite["chat_id"],
        user_id=current_user.id,
        role="member",
    )
    db.add(new_member)
    await db.commit()

    invite["use_count"] += 1

    return InviteJoinResponse(
        success=True,
        chat_id=invite["chat_id"],
        message="Вы успешно присоединились к чату",
    )


@router.get("/chat/{chat_id}", response_model=InviteListResponse)
async def list_chat_invites(
    chat_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> InviteListResponse:
    """Получить список приглашений чата."""
    member_result = await db.execute(
        select(ChatMember)
        .where(ChatMember.chat_id == chat_id)
        .where(ChatMember.user_id == current_user.id)
    )
    member = member_result.scalar_one_or_none()
    if not member or member.role not in ["owner", "admin"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={"message": "Нет прав для просмотра приглашений", "code": "no_permission"},
        )

    chat_invites = [
        InviteResponse(**inv)
        for inv in INVITES.values()
        if inv["chat_id"] == chat_id
    ]

    return InviteListResponse(invites=chat_invites, total=len(chat_invites))


@router.delete("/{code}", status_code=status.HTTP_204_NO_CONTENT)
async def revoke_invite(
    code: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> None:
    """Отозвать приглашение."""
    invite = INVITES.get(code)
    if not invite:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"message": "Приглашение не найдено", "code": "invite_not_found"},
        )

    member_result = await db.execute(
        select(ChatMember)
        .where(ChatMember.chat_id == invite["chat_id"])
        .where(ChatMember.user_id == current_user.id)
    )
    member = member_result.scalar_one_or_none()
    if not member or member.role not in ["owner", "admin"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={"message": "Нет прав для отзыва приглашения", "code": "no_permission"},
        )

    del INVITES[code]
