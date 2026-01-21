"""Тесты для поиска по сообщениям."""

import uuid
from datetime import datetime

import pytest

from src.schemas.search import (
    SearchRequest,
    SearchResponse,
    SearchResultItem,
    SearchType,
)


class TestSearchSchemas:
    """Тесты схем поиска."""

    def test_search_type_values(self) -> None:
        """Тест значений типа поиска."""
        assert SearchType.ALL.value == "all"
        assert SearchType.TEXT.value == "text"
        assert SearchType.MEDIA.value == "media"
        assert SearchType.VOICE.value == "voice"

    def test_search_request_minimal(self) -> None:
        """Тест минимального запроса поиска."""
        request = SearchRequest(query="привет")
        assert request.query == "привет"
        assert request.chat_id is None
        assert request.search_type == SearchType.ALL
        assert request.limit == 20
        assert request.offset == 0

    def test_search_request_full(self) -> None:
        """Тест полного запроса поиска."""
        chat_id = uuid.uuid4()
        sender_id = uuid.uuid4()
        request = SearchRequest(
            query="тест",
            chat_id=chat_id,
            search_type=SearchType.TEXT,
            sender_id=sender_id,
            limit=50,
            offset=10,
        )
        assert request.query == "тест"
        assert request.chat_id == chat_id
        assert request.search_type == SearchType.TEXT
        assert request.sender_id == sender_id
        assert request.limit == 50
        assert request.offset == 10

    def test_search_result_item(self) -> None:
        """Тест элемента результата поиска."""
        item = SearchResultItem(
            message_id=uuid.uuid4(),
            chat_id=uuid.uuid4(),
            chat_name="Тестовый чат",
            sender_id=uuid.uuid4(),
            sender_name="Иван",
            content="Привет, как дела?",
            highlight="...Привет, как дела?...",
            created_at=datetime.now(),
            has_media=False,
        )
        assert item.chat_name == "Тестовый чат"
        assert item.sender_name == "Иван"
        assert item.has_media is False

    def test_search_response(self) -> None:
        """Тест ответа поиска."""
        response = SearchResponse(
            query="привет",
            total_count=100,
            results=[
                SearchResultItem(
                    message_id=uuid.uuid4(),
                    chat_id=uuid.uuid4(),
                    chat_name="Чат",
                    sender_id=uuid.uuid4(),
                    sender_name="Иван",
                    content="Привет",
                    highlight="Привет",
                    created_at=datetime.now(),
                    has_media=False,
                )
            ],
            has_more=True,
        )
        assert response.query == "привет"
        assert response.total_count == 100
        assert len(response.results) == 1
        assert response.has_more is True

    def test_search_request_validation_empty_query(self) -> None:
        """Тест валидации пустого запроса."""
        with pytest.raises(ValueError):
            SearchRequest(query="")

    def test_search_request_validation_limit(self) -> None:
        """Тест валидации лимита."""
        with pytest.raises(ValueError):
            SearchRequest(query="test", limit=0)
        with pytest.raises(ValueError):
            SearchRequest(query="test", limit=101)
