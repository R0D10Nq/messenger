"""Initial schema.

Revision ID: 001
Revises: 
Create Date: 2026-01-21

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision: str = "001"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Users
    op.create_table(
        "users",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("email", sa.String(255), unique=True, nullable=False, index=True),
        sa.Column("password_hash", sa.String(255), nullable=False),
        sa.Column("name", sa.String(100), nullable=False),
        sa.Column("avatar_url", sa.String(500), nullable=True),
        sa.Column("bio", sa.Text, nullable=True),
        sa.Column("is_active", sa.Boolean, default=True, nullable=False),
        sa.Column("is_verified", sa.Boolean, default=False, nullable=False),
        sa.Column("totp_secret", sa.String(32), nullable=True),
        sa.Column("totp_enabled", sa.Boolean, default=False, nullable=False),
        sa.Column("totp_verified_at", sa.DateTime, nullable=True),
        sa.Column("created_at", sa.DateTime, server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime, onupdate=sa.func.now(), nullable=True),
    )

    # User Sessions
    op.create_table(
        "user_sessions",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("user_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True),
        sa.Column("refresh_token_hash", sa.String(255), nullable=False),
        sa.Column("device_info", sa.String(500), nullable=True),
        sa.Column("ip_address", sa.String(45), nullable=True),
        sa.Column("expires_at", sa.DateTime, nullable=False),
        sa.Column("created_at", sa.DateTime, server_default=sa.func.now(), nullable=False),
    )

    # Contacts
    op.create_table(
        "contacts",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("user_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True),
        sa.Column("contact_user_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
        sa.Column("nickname", sa.String(100), nullable=True),
        sa.Column("status", sa.String(20), default="pending", nullable=False),
        sa.Column("created_at", sa.DateTime, server_default=sa.func.now(), nullable=False),
        sa.UniqueConstraint("user_id", "contact_user_id", name="uq_contacts_user_contact"),
    )

    # Chats
    op.create_table(
        "chats",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("chat_type", sa.String(20), default="direct", nullable=False),
        sa.Column("name", sa.String(100), nullable=True),
        sa.Column("description", sa.Text, nullable=True),
        sa.Column("avatar_url", sa.String(500), nullable=True),
        sa.Column("created_at", sa.DateTime, server_default=sa.func.now(), nullable=False),
    )

    # Chat Members
    op.create_table(
        "chat_members",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("chat_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("chats.id", ondelete="CASCADE"), nullable=False, index=True),
        sa.Column("user_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True),
        sa.Column("role", sa.String(20), default="member", nullable=False),
        sa.Column("joined_at", sa.DateTime, server_default=sa.func.now(), nullable=False),
        sa.Column("last_read_at", sa.DateTime, nullable=True),
        sa.UniqueConstraint("chat_id", "user_id", name="uq_chat_members_chat_user"),
    )

    # Messages
    op.create_table(
        "messages",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("chat_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("chats.id", ondelete="CASCADE"), nullable=False, index=True),
        sa.Column("sender_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("users.id", ondelete="SET NULL"), nullable=True, index=True),
        sa.Column("content", sa.Text, nullable=False),
        sa.Column("status", sa.String(20), default="sent", nullable=False),
        sa.Column("reply_to_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("messages.id", ondelete="SET NULL"), nullable=True),
        sa.Column("is_edited", sa.Boolean, default=False, nullable=False),
        sa.Column("created_at", sa.DateTime, server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime, onupdate=sa.func.now(), nullable=True),
    )

    # Media Files
    op.create_table(
        "media_files",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("user_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True),
        sa.Column("filename", sa.String(255), nullable=False),
        sa.Column("original_filename", sa.String(255), nullable=False),
        sa.Column("media_type", sa.String(20), nullable=False),
        sa.Column("mime_type", sa.String(100), nullable=False),
        sa.Column("size_bytes", sa.BigInteger, nullable=False),
        sa.Column("storage_path", sa.String(500), nullable=False),
        sa.Column("created_at", sa.DateTime, server_default=sa.func.now(), nullable=False),
    )

    # Message Attachments
    op.create_table(
        "message_attachments",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("message_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("messages.id", ondelete="CASCADE"), nullable=False, index=True),
        sa.Column("media_file_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("media_files.id", ondelete="CASCADE"), nullable=False),
        sa.Column("created_at", sa.DateTime, server_default=sa.func.now(), nullable=False),
    )

    # Transcriptions
    op.create_table(
        "transcriptions",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("media_file_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("media_files.id", ondelete="CASCADE"), nullable=False, unique=True),
        sa.Column("status", sa.String(20), default="pending", nullable=False),
        sa.Column("text", sa.Text, nullable=True),
        sa.Column("language", sa.String(10), nullable=True),
        sa.Column("duration_seconds", sa.Float, nullable=True),
        sa.Column("error_message", sa.Text, nullable=True),
        sa.Column("created_at", sa.DateTime, server_default=sa.func.now(), nullable=False),
        sa.Column("completed_at", sa.DateTime, nullable=True),
    )

    # User Public Keys (E2E Encryption)
    op.create_table(
        "user_public_keys",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("user_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True),
        sa.Column("device_id", sa.String(100), nullable=False),
        sa.Column("identity_key", sa.Text, nullable=False),
        sa.Column("signed_prekey", sa.Text, nullable=False),
        sa.Column("signed_prekey_signature", sa.Text, nullable=False),
        sa.Column("created_at", sa.DateTime, server_default=sa.func.now(), nullable=False),
        sa.UniqueConstraint("user_id", "device_id", name="uq_user_public_keys_user_device"),
    )

    # One-Time Prekeys (E2E Encryption)
    op.create_table(
        "one_time_prekeys",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("user_public_key_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("user_public_keys.id", ondelete="CASCADE"), nullable=False, index=True),
        sa.Column("key_id", sa.Integer, nullable=False),
        sa.Column("prekey", sa.Text, nullable=False),
        sa.Column("is_used", sa.Boolean, default=False, nullable=False),
        sa.Column("created_at", sa.DateTime, server_default=sa.func.now(), nullable=False),
        sa.Column("used_at", sa.DateTime, nullable=True),
    )

    # Calls
    op.create_table(
        "calls",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("caller_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True),
        sa.Column("callee_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True),
        sa.Column("call_type", sa.String(20), default="audio", nullable=False),
        sa.Column("status", sa.String(20), default="pending", nullable=False),
        sa.Column("started_at", sa.DateTime, nullable=True),
        sa.Column("ended_at", sa.DateTime, nullable=True),
        sa.Column("duration_seconds", sa.Integer, nullable=True),
        sa.Column("end_reason", sa.String(50), nullable=True),
        sa.Column("created_at", sa.DateTime, server_default=sa.func.now(), nullable=False),
    )


def downgrade() -> None:
    op.drop_table("calls")
    op.drop_table("one_time_prekeys")
    op.drop_table("user_public_keys")
    op.drop_table("transcriptions")
    op.drop_table("message_attachments")
    op.drop_table("media_files")
    op.drop_table("messages")
    op.drop_table("chat_members")
    op.drop_table("chats")
    op.drop_table("contacts")
    op.drop_table("user_sessions")
    op.drop_table("users")
