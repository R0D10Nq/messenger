"""Модели для аудио/видео звонков."""

from __future__ import annotations

import uuid
from datetime import datetime
from enum import Enum
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, ForeignKey, String, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.db.base import Base

if TYPE_CHECKING:
    from src.models.user import User


class CallType(str, Enum):
    """Тип звонка."""

    AUDIO = "audio"
    VIDEO = "video"


class CallStatus(str, Enum):
    """Статус звонка."""

    PENDING = "pending"
    RINGING = "ringing"
    ACTIVE = "active"
    ENDED = "ended"
    MISSED = "missed"
    DECLINED = "declined"
    FAILED = "failed"


class Call(Base):
    """Модель звонка."""

    __tablename__ = "calls"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
    caller_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    callee_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    call_type: Mapped[str] = mapped_column(
        String(20),
        default=CallType.AUDIO.value,
        nullable=False,
    )
    status: Mapped[str] = mapped_column(
        String(20),
        default=CallStatus.PENDING.value,
        nullable=False,
    )
    started_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    ended_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    duration_seconds: Mapped[int | None] = mapped_column(nullable=True)
    end_reason: Mapped[str | None] = mapped_column(String(50), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        server_default=func.now(),
        nullable=False,
    )

    caller: Mapped[User] = relationship("User", foreign_keys=[caller_id])
    callee: Mapped[User] = relationship("User", foreign_keys=[callee_id])
