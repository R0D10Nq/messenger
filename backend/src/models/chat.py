"""Модели чатов и сообщений."""

from __future__ import annotations

import uuid
from datetime import datetime
from enum import Enum
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, ForeignKey, String, Text, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.db.base import Base

if TYPE_CHECKING:
    from src.models.user import User


class ChatType(str, Enum):
    """Тип чата."""

    DIRECT = "direct"
    GROUP = "group"


class MessageStatus(str, Enum):
    """Статус сообщения."""

    SENT = "sent"
    DELIVERED = "delivered"
    READ = "read"


class MemberRole(str, Enum):
    """Роль участника в групповом чате."""

    OWNER = "owner"
    ADMIN = "admin"
    MEMBER = "member"


class Chat(Base):
    """Модель чата."""

    __tablename__ = "chats"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
    chat_type: Mapped[str] = mapped_column(
        String(20),
        default=ChatType.DIRECT.value,
        nullable=False,
    )
    name: Mapped[str | None] = mapped_column(String(100), nullable=True)
    description: Mapped[str | None] = mapped_column(String(500), nullable=True)
    avatar_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
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

    members: Mapped[list[ChatMember]] = relationship(
        "ChatMember",
        back_populates="chat",
        cascade="all, delete-orphan",
    )
    messages: Mapped[list[Message]] = relationship(
        "Message",
        back_populates="chat",
        cascade="all, delete-orphan",
    )


class ChatMember(Base):
    """Участник чата."""

    __tablename__ = "chat_members"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
    chat_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("chats.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    role: Mapped[str] = mapped_column(
        String(20),
        default=MemberRole.MEMBER.value,
        nullable=False,
    )
    joined_at: Mapped[datetime] = mapped_column(
        DateTime,
        server_default=func.now(),
        nullable=False,
    )
    last_read_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)

    chat: Mapped[Chat] = relationship("Chat", back_populates="members")
    user: Mapped[User] = relationship("User")


class Message(Base):
    """Модель сообщения."""

    __tablename__ = "messages"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
    chat_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("chats.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    sender_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    content: Mapped[str] = mapped_column(Text, nullable=False)
    status: Mapped[str] = mapped_column(
        String(20),
        default=MessageStatus.SENT.value,
        nullable=False,
    )
    reply_to_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("messages.id", ondelete="SET NULL"),
        nullable=True,
    )
    edited_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        server_default=func.now(),
        nullable=False,
    )

    chat: Mapped[Chat] = relationship("Chat", back_populates="messages")
    sender: Mapped[User] = relationship("User")
    reply_to: Mapped[Message | None] = relationship(
        "Message",
        remote_side=[id],
        foreign_keys=[reply_to_id],
    )
