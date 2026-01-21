"""Тесты для упоминаний и превью ссылок."""

import uuid

from src.schemas.mention import LinkPreview, MentionData, MessageWithMentions, ParsedMessage
from src.services.mention import extract_urls


class TestMentionSchemas:
    """Тесты схем упоминаний."""

    def test_mention_data(self) -> None:
        """Тест данных упоминания."""
        mention = MentionData(
            user_id=uuid.uuid4(),
            user_name="Иван",
            offset=5,
            length=5,
        )
        assert mention.user_name == "Иван"
        assert mention.offset == 5
        assert mention.length == 5

    def test_link_preview(self) -> None:
        """Тест превью ссылки."""
        preview = LinkPreview(
            url="https://example.com",
            title="Пример",
            description="Описание страницы",
            image_url="https://example.com/image.jpg",
            site_name="Example",
        )
        assert preview.url == "https://example.com"
        assert preview.title == "Пример"

    def test_link_preview_minimal(self) -> None:
        """Тест минимального превью ссылки."""
        preview = LinkPreview(url="https://example.com")
        assert preview.url == "https://example.com"
        assert preview.title is None

    def test_message_with_mentions(self) -> None:
        """Тест сообщения с упоминаниями."""
        msg = MessageWithMentions(
            content="Привет @Иван!",
            mentions=[
                MentionData(
                    user_id=uuid.uuid4(),
                    user_name="Иван",
                    offset=7,
                    length=5,
                )
            ],
            link_previews=[],
        )
        assert len(msg.mentions) == 1
        assert msg.mentions[0].user_name == "Иван"

    def test_parsed_message(self) -> None:
        """Тест парсинга сообщения."""
        parsed = ParsedMessage(
            content="Привет @Иван, смотри https://example.com",
            mentions=[
                MentionData(
                    user_id=uuid.uuid4(),
                    user_name="Иван",
                    offset=7,
                    length=5,
                )
            ],
            urls=["https://example.com"],
        )
        assert len(parsed.mentions) == 1
        assert len(parsed.urls) == 1


class TestMentionService:
    """Тесты сервиса упоминаний."""

    def test_extract_urls_single(self) -> None:
        """Тест извлечения одного URL."""
        urls = extract_urls("Смотри https://example.com")
        assert len(urls) == 1
        assert urls[0] == "https://example.com"

    def test_extract_urls_multiple(self) -> None:
        """Тест извлечения нескольких URL."""
        urls = extract_urls("Ссылки: https://a.com и https://b.com/path")
        assert len(urls) == 2

    def test_extract_urls_none(self) -> None:
        """Тест текста без URL."""
        urls = extract_urls("Обычный текст без ссылок")
        assert len(urls) == 0

    def test_extract_urls_with_path(self) -> None:
        """Тест URL с путём."""
        urls = extract_urls("https://example.com/path/to/page?query=1")
        assert len(urls) == 1
        assert "path/to/page" in urls[0]
