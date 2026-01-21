"""Fix contacts schema - rename columns.

Revision ID: 006
Revises: 005
Create Date: 2026-01-21

"""

from typing import Sequence, Union

from alembic import op

revision: str = "006"
down_revision: Union[str, None] = "005"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Переименовываем колонки в contacts
    op.execute("ALTER TABLE contacts RENAME COLUMN user_id TO owner_id")
    op.execute("ALTER TABLE contacts RENAME COLUMN contact_user_id TO contact_id")
    
    # Удаляем старый constraint и создаём новый
    op.execute("ALTER TABLE contacts DROP CONSTRAINT IF EXISTS uq_contacts_user_contact")
    op.execute("""
        ALTER TABLE contacts 
        ADD CONSTRAINT uq_owner_contact UNIQUE (owner_id, contact_id)
    """)
    
    # Добавляем updated_at если нет
    op.execute("""
        DO $$ 
        BEGIN 
            IF NOT EXISTS (SELECT 1 FROM information_schema.columns 
                          WHERE table_name='contacts' AND column_name='updated_at') THEN
                ALTER TABLE contacts ADD COLUMN updated_at TIMESTAMP DEFAULT NOW();
            END IF;
        END $$;
    """)


def downgrade() -> None:
    op.execute("ALTER TABLE contacts RENAME COLUMN owner_id TO user_id")
    op.execute("ALTER TABLE contacts RENAME COLUMN contact_id TO contact_user_id")
    op.execute("ALTER TABLE contacts DROP CONSTRAINT IF EXISTS uq_owner_contact")
    op.execute("""
        ALTER TABLE contacts 
        ADD CONSTRAINT uq_contacts_user_contact UNIQUE (user_id, contact_user_id)
    """)
