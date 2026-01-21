"""Тесты для перевода сообщений."""

import uuid

import pytest


class TestTranslateSchemas:
    """Тесты схем перевода."""

    def test_translate_request(self):
        """TranslateRequest валидация."""
        from src.schemas.translate import TranslateRequest

        data = TranslateRequest(
            message_id=uuid.uuid4(),
            target_language="en",
        )
        assert data.target_language == "en"

    def test_translate_text_request(self):
        """TranslateTextRequest валидация."""
        from src.schemas.translate import TranslateTextRequest

        data = TranslateTextRequest(
            text="Привет, мир!",
            target_language="en",
            source_language="ru",
        )
        assert data.text == "Привет, мир!"
        assert data.target_language == "en"
        assert data.source_language == "ru"

    def test_translate_text_request_without_source(self):
        """TranslateTextRequest без source_language."""
        from src.schemas.translate import TranslateTextRequest

        data = TranslateTextRequest(
            text="Hello",
            target_language="ru",
        )
        assert data.source_language is None

    def test_translate_response(self):
        """TranslateResponse валидация."""
        from src.schemas.translate import TranslateResponse

        data = TranslateResponse(
            original_text="Hello",
            translated_text="Привет",
            source_language="en",
            target_language="ru",
            confidence=0.95,
        )
        assert data.original_text == "Hello"
        assert data.translated_text == "Привет"
        assert data.confidence == 0.95

    def test_translate_response_no_confidence(self):
        """TranslateResponse без confidence."""
        from src.schemas.translate import TranslateResponse

        data = TranslateResponse(
            original_text="Test",
            translated_text="Тест",
            source_language="en",
            target_language="ru",
        )
        assert data.confidence is None

    def test_detect_language_request(self):
        """DetectLanguageRequest валидация."""
        from src.schemas.translate import DetectLanguageRequest

        data = DetectLanguageRequest(text="Привет")
        assert data.text == "Привет"

    def test_detect_language_response(self):
        """DetectLanguageResponse валидация."""
        from src.schemas.translate import DetectLanguageResponse

        data = DetectLanguageResponse(
            language="ru",
            confidence=0.98,
            language_name="Русский",
        )
        assert data.language == "ru"
        assert data.language_name == "Русский"

    def test_supported_languages_response(self):
        """SupportedLanguagesResponse валидация."""
        from src.schemas.translate import SupportedLanguagesResponse

        data = SupportedLanguagesResponse(
            languages=[
                {"code": "ru", "name": "Русский"},
                {"code": "en", "name": "English"},
            ]
        )
        assert len(data.languages) == 2

    def test_supported_languages_list(self):
        """SUPPORTED_LANGUAGES содержит основные языки."""
        from src.schemas.translate import SUPPORTED_LANGUAGES

        codes = [l["code"] for l in SUPPORTED_LANGUAGES]
        assert "ru" in codes
        assert "en" in codes
        assert "de" in codes
        assert "fr" in codes
