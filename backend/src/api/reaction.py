"""API эндпоинты для реакций на сообщения."""

import uuid
from collections import defaultdict

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.deps import get_current_user
from src.db.session import get_db
from src.models.chat import ChatMember, Message
from src.models.reaction import MessageReaction
from src.models.user import User
from src.schemas.reaction import (
    MessageReactionsResponse,
    ReactionCreate,
    ReactionResponse,
    ReactionSummary,
)

router = APIRouter(prefix="/reactions", tags=["reactions"])


async def _check_message_access(
    message_id: uuid.UUID,
    user_id: uuid.UUID,
    db: AsyncSession,
) -> Message:
    """Проверить доступ к сообщению."""
    message = await db.get(Message, message_id)
    if not message:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Сообщение не найдено",
        )

    member = await db.scalar(
        select(ChatMember).where(
            ChatMember.chat_id == message.chat_id,
            ChatMember.user_id == user_id,
        )
    )
    if not member:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Нет доступа к этому чату",
        )

    return message


@router.post("/messages/{message_id}", response_model=ReactionResponse)
async def add_reaction(
    message_id: uuid.UUID,
    data: ReactionCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> ReactionResponse:
    """Добавить реакцию на сообщение."""
    await _check_message_access(message_id, current_user.id, db)

    existing = await db.scalar(
        select(MessageReaction).where(
            MessageReaction.message_id == message_id,
            MessageReaction.user_id == current_user.id,
            MessageReaction.emoji == data.emoji,
        )
    )
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Реакция уже добавлена",
        )

    reaction = MessageReaction(
        message_id=message_id,
        user_id=current_user.id,
        emoji=data.emoji,
    )
    db.add(reaction)
    await db.commit()
    await db.refresh(reaction)

    return ReactionResponse(
        id=reaction.id,
        message_id=reaction.message_id,
        user_id=reaction.user_id,
        user_name=current_user.name,
        emoji=reaction.emoji,
        created_at=reaction.created_at,
    )


@router.delete("/messages/{message_id}/{emoji}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_reaction(
    message_id: uuid.UUID,
    emoji: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> None:
    """Удалить реакцию с сообщения."""
    await _check_message_access(message_id, current_user.id, db)

    reaction = await db.scalar(
        select(MessageReaction).where(
            MessageReaction.message_id == message_id,
            MessageReaction.user_id == current_user.id,
            MessageReaction.emoji == emoji,
        )
    )
    if not reaction:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Реакция не найдена",
        )

    await db.delete(reaction)
    await db.commit()


@router.get("/messages/{message_id}", response_model=MessageReactionsResponse)
async def get_reactions(
    message_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> MessageReactionsResponse:
    """Получить все реакции на сообщение."""
    await _check_message_access(message_id, current_user.id, db)

    result = await db.execute(
        select(MessageReaction, User.name)
        .join(User, MessageReaction.user_id == User.id)
        .where(MessageReaction.message_id == message_id)
    )
    rows = result.all()

    emoji_counts: dict[str, int] = defaultdict(int)
    emoji_users: dict[str, list[str]] = defaultdict(list)
    emoji_my: dict[str, bool] = defaultdict(bool)

    for reaction, user_name in rows:
        emoji_counts[reaction.emoji] += 1
        emoji_users[reaction.emoji].append(user_name)
        if reaction.user_id == current_user.id:
            emoji_my[reaction.emoji] = True

    summaries = [
        ReactionSummary(
            emoji=emoji,
            count=emoji_counts[emoji],
            users=emoji_users[emoji][:5],
            reacted_by_me=emoji_my[emoji],
        )
        for emoji in emoji_counts
    ]

    return MessageReactionsResponse(
        message_id=message_id,
        reactions=summaries,
        total_count=len(rows),
    )
