"""API эндпоинты для поиска."""

import uuid
from collections.abc import Sequence
from typing import Any

from fastapi import APIRouter, Depends, Query
from sqlalchemy import and_, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.deps import get_current_user
from src.db.session import get_db
from src.models.chat import Chat, ChatMember, Message
from src.models.media import MessageAttachment
from src.models.user import User
from src.schemas.search import (
    SearchResponse,
    SearchResultItem,
    SearchType,
)

router = APIRouter(prefix="/search", tags=["search"])


def _highlight_text(content: str, query: str, max_len: int = 100) -> str:
    """Подсветить найденный текст."""
    query_lower = query.lower()
    content_lower = content.lower()

    idx = content_lower.find(query_lower)
    if idx == -1:
        return content[:max_len] + ("..." if len(content) > max_len else "")

    start = max(0, idx - 30)
    end = min(len(content), idx + len(query) + 30)

    prefix = "..." if start > 0 else ""
    suffix = "..." if end < len(content) else ""

    return prefix + content[start:end] + suffix


async def _get_chat_name(chat: Chat, current_user_id: uuid.UUID, db: AsyncSession) -> str:
    """Получить имя чата."""
    if chat.name:
        return chat.name

    for member in chat.members:
        if member.user_id != current_user_id:
            user = await db.get(User, member.user_id)
            if user:
                return user.name
    return "Чат"


@router.get("", response_model=SearchResponse)
async def search_messages(
    q: str = Query(..., min_length=1, max_length=500, description="Поисковый запрос"),
    chat_id: uuid.UUID | None = Query(None, description="ID чата"),
    search_type: SearchType = Query(SearchType.ALL, description="Тип поиска"),
    sender_id: uuid.UUID | None = Query(None, description="ID отправителя"),
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> SearchResponse:
    """Поиск по сообщениям."""
    user_chats_subq = (
        select(ChatMember.chat_id)
        .where(ChatMember.user_id == current_user.id)
        .scalar_subquery()
    )

    conditions: list[Any] = [Message.chat_id.in_(user_chats_subq)]

    if chat_id:
        conditions.append(Message.chat_id == chat_id)

    if sender_id:
        conditions.append(Message.sender_id == sender_id)

    if search_type == SearchType.TEXT:
        conditions.append(func.lower(Message.content).contains(q.lower()))
    elif search_type == SearchType.MEDIA:
        media_messages = select(MessageAttachment.message_id).scalar_subquery()
        conditions.append(Message.id.in_(media_messages))
        conditions.append(func.lower(Message.content).contains(q.lower()))
    elif search_type == SearchType.VOICE:
        conditions.append(func.lower(Message.content).contains(q.lower()))
    else:
        conditions.append(func.lower(Message.content).contains(q.lower()))

    count_query = select(func.count()).select_from(Message).where(and_(*conditions))
    total_count = await db.scalar(count_query) or 0

    query = (
        select(Message)
        .where(and_(*conditions))
        .order_by(Message.created_at.desc())
        .limit(limit)
        .offset(offset)
    )

    result = await db.execute(query)
    messages: Sequence[Message] = result.scalars().all()

    results: list[SearchResultItem] = []
    for msg in messages:
        chat = await db.get(Chat, msg.chat_id)
        sender = await db.get(User, msg.sender_id)

        if not chat or not sender:
            continue

        has_media_result = await db.execute(
            select(MessageAttachment.id).where(MessageAttachment.message_id == msg.id).limit(1)
        )
        has_media = has_media_result.scalar() is not None

        chat_name = await _get_chat_name(chat, current_user.id, db)

        results.append(
            SearchResultItem(
                message_id=msg.id,
                chat_id=msg.chat_id,
                chat_name=chat_name,
                sender_id=msg.sender_id,
                sender_name=sender.name,
                content=msg.content,
                highlight=_highlight_text(msg.content, q),
                created_at=msg.created_at,
                has_media=has_media,
            )
        )

    return SearchResponse(
        query=q,
        total_count=total_count,
        results=results,
        has_more=offset + limit < total_count,
    )
