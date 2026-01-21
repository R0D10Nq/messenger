"""API эндпоинты для закреплённых сообщений."""

import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.deps import get_current_user
from src.db.session import get_db
from src.models.chat import ChatMember, MemberRole, Message
from src.models.pin import PinnedMessage
from src.models.user import User
from src.schemas.pin import PinnedMessageResponse, PinnedMessagesListResponse

router = APIRouter(prefix="/chats", tags=["pinned"])


async def _check_chat_access(
    chat_id: uuid.UUID,
    user_id: uuid.UUID,
    db: AsyncSession,
    require_admin: bool = False,
) -> ChatMember:
    """Проверить доступ к чату."""
    member = await db.scalar(
        select(ChatMember).where(
            ChatMember.chat_id == chat_id,
            ChatMember.user_id == user_id,
        )
    )
    if not member:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Нет доступа к этому чату",
        )

    if require_admin and member.role == MemberRole.MEMBER.value:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Требуются права администратора",
        )

    return member


@router.post("/{chat_id}/pin/{message_id}", response_model=PinnedMessageResponse)
async def pin_message(
    chat_id: uuid.UUID,
    message_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> PinnedMessageResponse:
    """Закрепить сообщение."""
    await _check_chat_access(chat_id, current_user.id, db, require_admin=True)

    message = await db.get(Message, message_id)
    if not message or message.chat_id != chat_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Сообщение не найдено",
        )

    existing = await db.scalar(
        select(PinnedMessage).where(PinnedMessage.message_id == message_id)
    )
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Сообщение уже закреплено",
        )

    pinned = PinnedMessage(
        chat_id=chat_id,
        message_id=message_id,
        pinned_by=current_user.id,
    )
    db.add(pinned)
    await db.commit()
    await db.refresh(pinned)

    return PinnedMessageResponse(
        id=pinned.id,
        chat_id=pinned.chat_id,
        message_id=pinned.message_id,
        message_content=message.content,
        pinned_by_id=current_user.id,
        pinned_by_name=current_user.name,
        pinned_at=pinned.pinned_at,
    )


@router.delete("/{chat_id}/pin/{message_id}", status_code=status.HTTP_204_NO_CONTENT)
async def unpin_message(
    chat_id: uuid.UUID,
    message_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> None:
    """Открепить сообщение."""
    await _check_chat_access(chat_id, current_user.id, db, require_admin=True)

    pinned = await db.scalar(
        select(PinnedMessage).where(
            PinnedMessage.chat_id == chat_id,
            PinnedMessage.message_id == message_id,
        )
    )
    if not pinned:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Сообщение не закреплено",
        )

    await db.delete(pinned)
    await db.commit()


@router.get("/{chat_id}/pinned", response_model=PinnedMessagesListResponse)
async def get_pinned_messages(
    chat_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> PinnedMessagesListResponse:
    """Получить закреплённые сообщения чата."""
    await _check_chat_access(chat_id, current_user.id, db)

    result = await db.execute(
        select(PinnedMessage)
        .where(PinnedMessage.chat_id == chat_id)
        .order_by(PinnedMessage.pinned_at.desc())
    )
    pinned_list = result.scalars().all()

    responses = []
    for pinned in pinned_list:
        message = await db.get(Message, pinned.message_id)
        user = await db.get(User, pinned.pinned_by)

        if message and user:
            responses.append(
                PinnedMessageResponse(
                    id=pinned.id,
                    chat_id=pinned.chat_id,
                    message_id=pinned.message_id,
                    message_content=message.content,
                    pinned_by_id=user.id,
                    pinned_by_name=user.name,
                    pinned_at=pinned.pinned_at,
                )
            )

    return PinnedMessagesListResponse(
        chat_id=chat_id,
        pinned_messages=responses,
        count=len(responses),
    )
