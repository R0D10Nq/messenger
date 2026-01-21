"""API эндпоинты для перевода сообщений."""

import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.deps import get_current_user
from src.db import get_db
from src.models.chat import Message
from src.models.user import User
from src.schemas.translate import (
    DetectLanguageRequest,
    DetectLanguageResponse,
    SupportedLanguagesResponse,
    SUPPORTED_LANGUAGES,
    TranslateRequest,
    TranslateResponse,
    TranslateTextRequest,
)

router = APIRouter(prefix="/translate", tags=["translate"])

DEMO_TRANSLATIONS = {
    "ru": {
        "Hello": "Привет",
        "How are you?": "Как дела?",
        "Good morning": "Доброе утро",
        "Thank you": "Спасибо",
    },
    "en": {
        "Привет": "Hello",
        "Как дела?": "How are you?",
        "Доброе утро": "Good morning",
        "Спасибо": "Thank you",
    },
}


def detect_language(text: str) -> tuple[str, float]:
    """Определение языка текста (заглушка)."""
    cyrillic_count = sum(1 for c in text if '\u0400' <= c <= '\u04ff')
    latin_count = sum(1 for c in text if 'a' <= c.lower() <= 'z')

    if cyrillic_count > latin_count:
        return "ru", 0.95
    return "en", 0.90


def translate_text(text: str, source_lang: str, target_lang: str) -> str:
    """Перевод текста (заглушка)."""
    if target_lang in DEMO_TRANSLATIONS:
        if text in DEMO_TRANSLATIONS[target_lang]:
            return DEMO_TRANSLATIONS[target_lang][text]

    return f"[Перевод на {target_lang}] {text}"


@router.post("/message", response_model=TranslateResponse)
async def translate_message(
    request: TranslateRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> TranslateResponse:
    """Перевести сообщение."""
    message = await db.get(Message, request.message_id)
    if not message:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"message": "Сообщение не найдено", "code": "message_not_found"},
        )

    source_lang, confidence = detect_language(message.content)
    translated = translate_text(message.content, source_lang, request.target_language)

    return TranslateResponse(
        original_text=message.content,
        translated_text=translated,
        source_language=source_lang,
        target_language=request.target_language,
        confidence=confidence,
    )


@router.post("/text", response_model=TranslateResponse)
async def translate_text_endpoint(
    request: TranslateTextRequest,
    current_user: User = Depends(get_current_user),
) -> TranslateResponse:
    """Перевести произвольный текст."""
    if request.source_language:
        source_lang = request.source_language
        confidence = 1.0
    else:
        source_lang, confidence = detect_language(request.text)

    translated = translate_text(request.text, source_lang, request.target_language)

    return TranslateResponse(
        original_text=request.text,
        translated_text=translated,
        source_language=source_lang,
        target_language=request.target_language,
        confidence=confidence,
    )


@router.post("/detect", response_model=DetectLanguageResponse)
async def detect_language_endpoint(
    request: DetectLanguageRequest,
    current_user: User = Depends(get_current_user),
) -> DetectLanguageResponse:
    """Определить язык текста."""
    lang_code, confidence = detect_language(request.text)

    lang_name = next(
        (l["name"] for l in SUPPORTED_LANGUAGES if l["code"] == lang_code),
        lang_code,
    )

    return DetectLanguageResponse(
        language=lang_code,
        confidence=confidence,
        language_name=lang_name,
    )


@router.get("/languages", response_model=SupportedLanguagesResponse)
async def get_supported_languages(
    current_user: User = Depends(get_current_user),
) -> SupportedLanguagesResponse:
    """Получить список поддерживаемых языков."""
    return SupportedLanguagesResponse(languages=SUPPORTED_LANGUAGES)
