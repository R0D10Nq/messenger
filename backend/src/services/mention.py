"""Сервис для парсинга упоминаний и ссылок."""

import re
import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.user import User
from src.schemas.mention import LinkPreview, MentionData, ParsedMessage

MENTION_PATTERN = re.compile(r"@(\w+)")
URL_PATTERN = re.compile(
    r"https?://(?:[-\w.])+(?::\d+)?(?:/[-\w._~:/?#\[\]@!$&'()*+,;=%]*)?"
)


async def parse_mentions(
    content: str,
    chat_member_ids: list[uuid.UUID],
    db: AsyncSession,
) -> list[MentionData]:
    """Парсить упоминания в тексте."""
    mentions: list[MentionData] = []

    for match in MENTION_PATTERN.finditer(content):
        username = match.group(1)

        user = await db.scalar(
            select(User).where(
                User.name.ilike(username),
                User.id.in_(chat_member_ids),
            )
        )

        if user:
            mentions.append(
                MentionData(
                    user_id=user.id,
                    user_name=user.name,
                    offset=match.start(),
                    length=len(match.group(0)),
                )
            )

    return mentions


def extract_urls(content: str) -> list[str]:
    """Извлечь URL из текста."""
    return URL_PATTERN.findall(content)


async def parse_message(
    content: str,
    chat_member_ids: list[uuid.UUID],
    db: AsyncSession,
) -> ParsedMessage:
    """Парсить сообщение для упоминаний и URL."""
    mentions = await parse_mentions(content, chat_member_ids, db)
    urls = extract_urls(content)

    return ParsedMessage(
        content=content,
        mentions=mentions,
        urls=urls,
    )


async def fetch_link_preview(url: str) -> LinkPreview | None:
    """Получить превью ссылки (заглушка)."""
    return LinkPreview(
        url=url,
        title=None,
        description=None,
        image_url=None,
        site_name=None,
    )
