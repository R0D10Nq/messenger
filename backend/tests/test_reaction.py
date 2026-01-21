"""Тесты для реакций на сообщения."""

import uuid
from datetime import datetime

import pytest

from src.schemas.reaction import (
    MessageReactionsResponse,
    ReactionCreate,
    ReactionResponse,
    ReactionSummary,
)


class TestReactionSchemas:
    """Тесты схем реакций."""

    def test_reaction_create(self) -> None:
        """Тест создания реакции."""
        data = ReactionCreate(emoji="👍")
        assert data.emoji == "👍"

    def test_reaction_create_unicode(self) -> None:
        """Тест создания реакции с unicode эмодзи."""
        data = ReactionCreate(emoji="🎉")
        assert data.emoji == "🎉"

    def test_reaction_response(self) -> None:
        """Тест ответа реакции."""
        response = ReactionResponse(
            id=uuid.uuid4(),
            message_id=uuid.uuid4(),
            user_id=uuid.uuid4(),
            user_name="Иван",
            emoji="❤️",
            created_at=datetime.now(),
        )
        assert response.emoji == "❤️"
        assert response.user_name == "Иван"

    def test_reaction_summary(self) -> None:
        """Тест сводки реакций."""
        summary = ReactionSummary(
            emoji="👍",
            count=5,
            users=["Иван", "Мария", "Петр"],
            reacted_by_me=True,
        )
        assert summary.count == 5
        assert len(summary.users) == 3
        assert summary.reacted_by_me is True

    def test_message_reactions_response(self) -> None:
        """Тест ответа со всеми реакциями."""
        response = MessageReactionsResponse(
            message_id=uuid.uuid4(),
            reactions=[
                ReactionSummary(emoji="👍", count=3, users=["Иван"], reacted_by_me=True),
                ReactionSummary(emoji="❤️", count=2, users=["Мария"], reacted_by_me=False),
            ],
            total_count=5,
        )
        assert len(response.reactions) == 2
        assert response.total_count == 5

    def test_reaction_create_validation(self) -> None:
        """Тест валидации создания реакции."""
        with pytest.raises(ValueError):
            ReactionCreate(emoji="")
