"""API эндпоинты для транскрипции голосовых сообщений."""

import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.deps import get_current_user
from src.db import get_db
from src.models.media import MediaFile, MediaType, Transcription
from src.models.user import User
from src.schemas.media import CreateTranscriptionRequest, TranscriptionResponse
from src.services.transcription import TranscriptionService

router = APIRouter(prefix="/transcriptions", tags=["transcriptions"])


def _build_transcription_response(transcription: Transcription) -> TranscriptionResponse:
    """Построить ответ транскрипции."""
    return TranscriptionResponse(
        id=transcription.id,
        media_id=transcription.media_id,
        status=transcription.status,
        text=transcription.text,
        language=transcription.language,
        duration_seconds=transcription.duration_seconds,
        error_message=transcription.error_message,
        created_at=transcription.created_at,
        completed_at=transcription.completed_at,
    )


@router.post("", response_model=TranscriptionResponse, status_code=status.HTTP_201_CREATED)
async def create_transcription(
    data: CreateTranscriptionRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> TranscriptionResponse:
    """Создать транскрипцию для голосового сообщения."""
    media = await db.get(MediaFile, data.media_id)

    if not media:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"message": "Медиафайл не найден", "code": "media_not_found"},
        )

    if media.media_type != MediaType.VOICE.value:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "message": "Транскрипция доступна только для голосовых сообщений",
                "code": "not_voice",
            },
        )

    service = TranscriptionService(db)

    try:
        transcription = await service.create_transcription(data.media_id)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"message": str(e), "code": "transcription_error"},
        ) from e

    return _build_transcription_response(transcription)


@router.get("/{transcription_id}", response_model=TranscriptionResponse)
async def get_transcription(
    transcription_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> TranscriptionResponse:
    """Получить транскрипцию по ID."""
    service = TranscriptionService(db)
    transcription = await service.get_transcription_by_id(transcription_id)

    if not transcription:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"message": "Транскрипция не найдена", "code": "not_found"},
        )

    return _build_transcription_response(transcription)


@router.get("/media/{media_id}", response_model=TranscriptionResponse)
async def get_transcription_by_media(
    media_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> TranscriptionResponse:
    """Получить транскрипцию по ID медиафайла."""
    service = TranscriptionService(db)
    transcription = await service.get_transcription(media_id)

    if not transcription:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"message": "Транскрипция не найдена", "code": "not_found"},
        )

    return _build_transcription_response(transcription)


@router.post("/{transcription_id}/process", response_model=TranscriptionResponse)
async def process_transcription(
    transcription_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> TranscriptionResponse:
    """Запустить обработку транскрипции."""
    service = TranscriptionService(db)
    transcription = await service.process_transcription(transcription_id)

    if not transcription:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"message": "Транскрипция не найдена", "code": "not_found"},
        )

    return _build_transcription_response(transcription)
