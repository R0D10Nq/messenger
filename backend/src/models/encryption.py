"""Модели для E2E шифрования [SECURITY]."""

from __future__ import annotations

import uuid
from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, ForeignKey, String, Text, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.db.base import Base

if TYPE_CHECKING:
    from src.models.user import User


class UserPublicKey(Base):
    """Публичный ключ пользователя для E2E шифрования."""

    __tablename__ = "user_public_keys"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    device_id: Mapped[str] = mapped_column(String(100), nullable=False)
    identity_key: Mapped[str] = mapped_column(Text, nullable=False)
    signed_prekey: Mapped[str] = mapped_column(Text, nullable=False)
    signed_prekey_signature: Mapped[str] = mapped_column(Text, nullable=False)
    is_active: Mapped[bool] = mapped_column(default=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        server_default=func.now(),
        nullable=False,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    user: Mapped[User] = relationship("User")


class OneTimePrekey(Base):
    """Одноразовый prekey для установки сессии."""

    __tablename__ = "one_time_prekeys"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
    user_public_key_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("user_public_keys.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    key_id: Mapped[int] = mapped_column(nullable=False)
    prekey: Mapped[str] = mapped_column(Text, nullable=False)
    used: Mapped[bool] = mapped_column(default=False, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        server_default=func.now(),
        nullable=False,
    )

    user_public_key: Mapped[UserPublicKey] = relationship("UserPublicKey")
