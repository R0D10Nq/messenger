"""Тесты для закреплённых сообщений."""

import uuid
from datetime import datetime

from src.schemas.pin import PinnedMessageResponse, PinnedMessagesListResponse


class TestPinSchemas:
    """Тесты схем закреплённых сообщений."""

    def test_pinned_message_response(self) -> None:
        """Тест ответа закреплённого сообщения."""
        response = PinnedMessageResponse(
            id=uuid.uuid4(),
            chat_id=uuid.uuid4(),
            message_id=uuid.uuid4(),
            message_content="Важное сообщение",
            pinned_by_id=uuid.uuid4(),
            pinned_by_name="Иван",
            pinned_at=datetime.now(),
        )
        assert response.message_content == "Важное сообщение"
        assert response.pinned_by_name == "Иван"

    def test_pinned_messages_list_response(self) -> None:
        """Тест списка закреплённых сообщений."""
        chat_id = uuid.uuid4()
        response = PinnedMessagesListResponse(
            chat_id=chat_id,
            pinned_messages=[
                PinnedMessageResponse(
                    id=uuid.uuid4(),
                    chat_id=chat_id,
                    message_id=uuid.uuid4(),
                    message_content="Первое закреплённое",
                    pinned_by_id=uuid.uuid4(),
                    pinned_by_name="Иван",
                    pinned_at=datetime.now(),
                ),
                PinnedMessageResponse(
                    id=uuid.uuid4(),
                    chat_id=chat_id,
                    message_id=uuid.uuid4(),
                    message_content="Второе закреплённое",
                    pinned_by_id=uuid.uuid4(),
                    pinned_by_name="Мария",
                    pinned_at=datetime.now(),
                ),
            ],
            count=2,
        )
        assert response.count == 2
        assert len(response.pinned_messages) == 2

    def test_pinned_messages_empty_list(self) -> None:
        """Тест пустого списка закреплённых сообщений."""
        response = PinnedMessagesListResponse(
            chat_id=uuid.uuid4(),
            pinned_messages=[],
            count=0,
        )
        assert response.count == 0
        assert len(response.pinned_messages) == 0
