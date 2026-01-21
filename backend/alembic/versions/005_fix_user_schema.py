"""Fix user schema - add missing columns.

Revision ID: 005
Revises: 004
Create Date: 2026-01-21

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "005"
down_revision: Union[str, None] = "004"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Удаляем bio если есть, добавляем status_message
    op.execute("ALTER TABLE users DROP COLUMN IF EXISTS bio")
    op.add_column("users", sa.Column("status_message", sa.String(200), nullable=True))
    
    # Добавляем email_verified_at если нет
    op.execute("""
        DO $$ 
        BEGIN 
            IF NOT EXISTS (SELECT 1 FROM information_schema.columns 
                          WHERE table_name='users' AND column_name='email_verified_at') THEN
                ALTER TABLE users ADD COLUMN email_verified_at TIMESTAMP;
            END IF;
        END $$;
    """)
    
    # Добавляем last_used_at в user_sessions если нет
    op.execute("""
        DO $$ 
        BEGIN 
            IF NOT EXISTS (SELECT 1 FROM information_schema.columns 
                          WHERE table_name='user_sessions' AND column_name='last_used_at') THEN
                ALTER TABLE user_sessions ADD COLUMN last_used_at TIMESTAMP DEFAULT NOW();
            END IF;
        END $$;
    """)


def downgrade() -> None:
    op.drop_column("users", "status_message")
    op.add_column("users", sa.Column("bio", sa.Text, nullable=True))
