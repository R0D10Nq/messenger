"""API эндпоинты для каналов."""

import uuid
from datetime import UTC, datetime

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.deps import get_current_user
from src.db import get_db
from src.models.user import User
from src.schemas.channel import (
    ChannelMemberResponse,
    ChannelPostRequest,
    ChannelPostResponse,
    ChannelResponse,
    ChannelRole,
    ChannelStatsResponse,
    ChannelType,
    ChannelUpdateRequest,
    CreateChannelRequest,
    ScheduledPostResponse,
)

router = APIRouter(prefix="/channels", tags=["channels"])

CHANNELS: dict[str, dict] = {}
CHANNEL_POSTS: dict[str, list[dict]] = {}
CHANNEL_MEMBERS: dict[str, list[dict]] = {}


@router.post("", response_model=ChannelResponse)
async def create_channel(
    request: CreateChannelRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> ChannelResponse:
    """Создать канал."""
    for ch in CHANNELS.values():
        if ch["username"] == request.username:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail={"message": "Это имя пользователя уже занято", "code": "username_taken"},
            )

    channel_id = uuid.uuid4()
    now = datetime.now(UTC)

    channel = {
        "id": channel_id,
        "name": request.name,
        "username": request.username,
        "description": request.description,
        "channel_type": request.channel_type,
        "owner_id": current_user.id,
        "subscriber_count": 1,
        "allow_comments": request.allow_comments,
        "created_at": now,
    }

    CHANNELS[str(channel_id)] = channel
    CHANNEL_POSTS[str(channel_id)] = []
    CHANNEL_MEMBERS[str(channel_id)] = [{
        "user_id": current_user.id,
        "username": current_user.username,
        "role": ChannelRole.OWNER,
        "joined_at": now,
    }]

    return ChannelResponse(**channel)


@router.get("/{channel_id}", response_model=ChannelResponse)
async def get_channel(
    channel_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
) -> ChannelResponse:
    """Получить информацию о канале."""
    channel = CHANNELS.get(str(channel_id))
    if not channel:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"message": "Канал не найден", "code": "channel_not_found"},
        )

    return ChannelResponse(**channel)


@router.put("/{channel_id}", response_model=ChannelResponse)
async def update_channel(
    channel_id: uuid.UUID,
    request: ChannelUpdateRequest,
    current_user: User = Depends(get_current_user),
) -> ChannelResponse:
    """Обновить канал."""
    channel = CHANNELS.get(str(channel_id))
    if not channel:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"message": "Канал не найден", "code": "channel_not_found"},
        )

    if channel["owner_id"] != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={"message": "Нет прав для редактирования", "code": "no_permission"},
        )

    if request.name is not None:
        channel["name"] = request.name
    if request.description is not None:
        channel["description"] = request.description
    if request.allow_comments is not None:
        channel["allow_comments"] = request.allow_comments

    return ChannelResponse(**channel)


@router.get("/{channel_id}/stats", response_model=ChannelStatsResponse)
async def get_channel_stats(
    channel_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
) -> ChannelStatsResponse:
    """Получить статистику канала."""
    channel = CHANNELS.get(str(channel_id))
    if not channel:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"message": "Канал не найден", "code": "channel_not_found"},
        )

    posts = CHANNEL_POSTS.get(str(channel_id), [])
    total_views = sum(p.get("views", 0) for p in posts)
    avg_views = total_views / len(posts) if posts else 0

    return ChannelStatsResponse(
        subscriber_count=channel["subscriber_count"],
        total_posts=len(posts),
        total_views=total_views,
        avg_views_per_post=avg_views,
        growth_rate=5.2,
        top_posts=posts[:5],
    )


@router.post("/{channel_id}/posts", response_model=ChannelPostResponse)
async def create_post(
    channel_id: uuid.UUID,
    request: ChannelPostRequest,
    current_user: User = Depends(get_current_user),
) -> ChannelPostResponse:
    """Создать публикацию в канале."""
    channel = CHANNELS.get(str(channel_id))
    if not channel:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"message": "Канал не найден", "code": "channel_not_found"},
        )

    members = CHANNEL_MEMBERS.get(str(channel_id), [])
    user_member = next((m for m in members if m["user_id"] == current_user.id), None)
    if not user_member or user_member["role"] not in [ChannelRole.OWNER, ChannelRole.ADMIN]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={"message": "Нет прав для публикации", "code": "no_permission"},
        )

    post_id = uuid.uuid4()
    now = datetime.now(UTC)

    post = {
        "id": post_id,
        "channel_id": channel_id,
        "content": request.content,
        "author_id": current_user.id,
        "views": 0,
        "is_pinned": request.pin,
        "created_at": now,
    }

    CHANNEL_POSTS[str(channel_id)].append(post)

    return ChannelPostResponse(**post)


@router.get("/{channel_id}/members", response_model=list[ChannelMemberResponse])
async def list_channel_members(
    channel_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
) -> list[ChannelMemberResponse]:
    """Получить список участников канала."""
    channel = CHANNELS.get(str(channel_id))
    if not channel:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"message": "Канал не найден", "code": "channel_not_found"},
        )

    members = CHANNEL_MEMBERS.get(str(channel_id), [])
    return [ChannelMemberResponse(**m) for m in members]


@router.post("/{channel_id}/subscribe", status_code=status.HTTP_204_NO_CONTENT)
async def subscribe_channel(
    channel_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
) -> None:
    """Подписаться на канал."""
    channel = CHANNELS.get(str(channel_id))
    if not channel:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"message": "Канал не найден", "code": "channel_not_found"},
        )

    members = CHANNEL_MEMBERS.get(str(channel_id), [])
    if any(m["user_id"] == current_user.id for m in members):
        return

    members.append({
        "user_id": current_user.id,
        "username": current_user.username,
        "role": ChannelRole.SUBSCRIBER,
        "joined_at": datetime.now(UTC),
    })

    channel["subscriber_count"] += 1


@router.delete("/{channel_id}/subscribe", status_code=status.HTTP_204_NO_CONTENT)
async def unsubscribe_channel(
    channel_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
) -> None:
    """Отписаться от канала."""
    channel = CHANNELS.get(str(channel_id))
    if not channel:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"message": "Канал не найден", "code": "channel_not_found"},
        )

    members = CHANNEL_MEMBERS.get(str(channel_id), [])
    for i, m in enumerate(members):
        if m["user_id"] == current_user.id and m["role"] != ChannelRole.OWNER:
            members.pop(i)
            channel["subscriber_count"] -= 1
            break
