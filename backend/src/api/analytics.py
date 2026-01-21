"""API эндпоинты для аналитики."""

import random
import uuid
from datetime import UTC, datetime, timedelta

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.deps import get_current_user
from src.db import get_db
from src.models.user import User
from src.schemas.analytics import (
    AnalyticsPeriod,
    AnalyticsRequest,
    ChatAnalyticsResponse,
    DataPoint,
    MetricSummary,
    OverviewResponse,
    UserActivityResponse,
)

router = APIRouter(prefix="/analytics", tags=["analytics"])


def generate_data_points(days: int) -> list[DataPoint]:
    """Генерирует демо-данные для графика."""
    now = datetime.now(UTC)
    points = []
    for i in range(days):
        date = now - timedelta(days=days - i - 1)
        value = random.randint(10, 100)
        points.append(DataPoint(timestamp=date, value=value))
    return points


def calculate_change(current: float, previous: float) -> tuple[float, str]:
    """Вычисляет изменение в процентах и тренд."""
    if previous == 0:
        return 0.0, "stable"
    change = ((current - previous) / previous) * 100
    trend = "up" if change > 0 else "down" if change < 0 else "stable"
    return round(change, 1), trend


@router.get("/overview", response_model=OverviewResponse)
async def get_overview(
    period: AnalyticsPeriod = AnalyticsPeriod.WEEK,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> OverviewResponse:
    """Получить общую сводку аналитики."""
    messages_current = random.randint(500, 1500)
    messages_prev = random.randint(400, 1200)
    msg_change, msg_trend = calculate_change(messages_current, messages_prev)

    users_current = random.randint(50, 200)
    users_prev = random.randint(40, 180)
    users_change, users_trend = calculate_change(users_current, users_prev)

    chats_current = random.randint(10, 50)
    chats_prev = random.randint(8, 45)
    chats_change, chats_trend = calculate_change(chats_current, chats_prev)

    media_current = random.randint(100, 500)
    media_prev = random.randint(80, 400)
    media_change, media_trend = calculate_change(media_current, media_prev)

    return OverviewResponse(
        messages=MetricSummary(
            current=messages_current,
            previous=messages_prev,
            change_percent=msg_change,
            trend=msg_trend,
        ),
        active_users=MetricSummary(
            current=users_current,
            previous=users_prev,
            change_percent=users_change,
            trend=users_trend,
        ),
        new_chats=MetricSummary(
            current=chats_current,
            previous=chats_prev,
            change_percent=chats_change,
            trend=chats_trend,
        ),
        media_shared=MetricSummary(
            current=media_current,
            previous=media_prev,
            change_percent=media_change,
            trend=media_trend,
        ),
    )


@router.get("/user", response_model=UserActivityResponse)
async def get_user_activity(
    period: AnalyticsPeriod = AnalyticsPeriod.WEEK,
    current_user: User = Depends(get_current_user),
) -> UserActivityResponse:
    """Получить аналитику активности пользователя."""
    days = {"day": 1, "week": 7, "month": 30, "year": 365}.get(period.value, 7)

    active_hours = {h: random.randint(0, 50) for h in range(24)}

    return UserActivityResponse(
        total_messages=random.randint(100, 1000),
        total_chats=random.randint(5, 30),
        total_media=random.randint(20, 200),
        total_calls=random.randint(0, 20),
        messages_by_day=generate_data_points(days),
        active_hours=active_hours,
        most_active_chat_id=str(uuid.uuid4()),
    )


@router.get("/chat/{chat_id}", response_model=ChatAnalyticsResponse)
async def get_chat_analytics(
    chat_id: uuid.UUID,
    period: AnalyticsPeriod = AnalyticsPeriod.WEEK,
    current_user: User = Depends(get_current_user),
) -> ChatAnalyticsResponse:
    """Получить аналитику чата."""
    days = {"day": 1, "week": 7, "month": 30, "year": 365}.get(period.value, 7)

    top_senders = [
        {"user_id": str(uuid.uuid4()), "username": f"user_{i}", "count": random.randint(50, 200)}
        for i in range(5)
    ]

    peak_hours = sorted(random.sample(range(24), 5))

    return ChatAnalyticsResponse(
        message_count=random.randint(500, 5000),
        member_count=random.randint(2, 100),
        media_count=random.randint(50, 500),
        messages_by_day=generate_data_points(days),
        top_senders=top_senders,
        peak_hours=peak_hours,
        avg_messages_per_day=round(random.uniform(10, 100), 1),
    )


@router.post("/export")
async def export_analytics(
    request: AnalyticsRequest,
    current_user: User = Depends(get_current_user),
) -> dict:
    """Экспортировать аналитику."""
    return {
        "status": "pending",
        "download_url": f"/api/analytics/download/{uuid.uuid4()}",
        "expires_at": (datetime.now(UTC) + timedelta(hours=24)).isoformat(),
    }
