"""Схемы для перевода сообщений."""

import uuid

from pydantic import BaseModel, Field


class TranslateRequest(BaseModel):
    """Запрос на перевод сообщения."""

    message_id: uuid.UUID
    target_language: str = Field(..., min_length=2, max_length=5)


class TranslateTextRequest(BaseModel):
    """Запрос на перевод текста."""

    text: str = Field(..., min_length=1, max_length=5000)
    target_language: str = Field(..., min_length=2, max_length=5)
    source_language: str | None = Field(None, min_length=2, max_length=5)


class TranslateResponse(BaseModel):
    """Ответ с переводом."""

    original_text: str
    translated_text: str
    source_language: str
    target_language: str
    confidence: float | None = None


class DetectLanguageRequest(BaseModel):
    """Запрос на определение языка."""

    text: str = Field(..., min_length=1, max_length=1000)


class DetectLanguageResponse(BaseModel):
    """Ответ с определённым языком."""

    language: str
    confidence: float
    language_name: str


class SupportedLanguagesResponse(BaseModel):
    """Список поддерживаемых языков."""

    languages: list[dict]


SUPPORTED_LANGUAGES = [
    {"code": "ru", "name": "Русский"},
    {"code": "en", "name": "English"},
    {"code": "de", "name": "Deutsch"},
    {"code": "fr", "name": "Français"},
    {"code": "es", "name": "Español"},
    {"code": "it", "name": "Italiano"},
    {"code": "pt", "name": "Português"},
    {"code": "zh", "name": "中文"},
    {"code": "ja", "name": "日本語"},
    {"code": "ko", "name": "한국어"},
    {"code": "ar", "name": "العربية"},
    {"code": "hi", "name": "हिन्दी"},
    {"code": "tr", "name": "Türkçe"},
    {"code": "pl", "name": "Polski"},
    {"code": "uk", "name": "Українська"},
]
