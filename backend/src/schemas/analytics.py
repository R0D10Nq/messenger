"""Схемы для аналитики."""

from datetime import datetime
from enum import Enum

from pydantic import BaseModel, Field


class AnalyticsPeriod(str, Enum):
    """Период аналитики."""

    DAY = "day"
    WEEK = "week"
    MONTH = "month"
    YEAR = "year"


class MetricType(str, Enum):
    """Тип метрики."""

    MESSAGES = "messages"
    USERS = "users"
    CHATS = "chats"
    MEDIA = "media"
    CALLS = "calls"


class DataPoint(BaseModel):
    """Точка данных для графика."""

    timestamp: datetime
    value: float


class MetricSummary(BaseModel):
    """Сводка по метрике."""

    current: float
    previous: float
    change_percent: float
    trend: str


class UserActivityResponse(BaseModel):
    """Активность пользователя."""

    total_messages: int
    total_chats: int
    total_media: int
    total_calls: int
    messages_by_day: list[DataPoint]
    active_hours: dict[int, int]
    most_active_chat_id: str | None


class ChatAnalyticsResponse(BaseModel):
    """Аналитика чата."""

    message_count: int
    member_count: int
    media_count: int
    messages_by_day: list[DataPoint]
    top_senders: list[dict]
    peak_hours: list[int]
    avg_messages_per_day: float


class OverviewResponse(BaseModel):
    """Общая сводка."""

    messages: MetricSummary
    active_users: MetricSummary
    new_chats: MetricSummary
    media_shared: MetricSummary


class AnalyticsRequest(BaseModel):
    """Запрос аналитики."""

    period: AnalyticsPeriod = AnalyticsPeriod.WEEK
    start_date: datetime | None = None
    end_date: datetime | None = None


class ExportAnalyticsRequest(BaseModel):
    """Запрос на экспорт аналитики."""

    period: AnalyticsPeriod
    format: str = Field("csv", pattern="^(csv|json|xlsx)$")
    metrics: list[MetricType] | None = None
