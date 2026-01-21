"""API эндпоинты для субтитров видео."""

import uuid
from datetime import UTC, datetime

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.deps import get_current_user
from src.db import get_db
from src.models.user import User
from src.schemas.subtitle import (
    GenerateSubtitlesRequest,
    SubtitleCue,
    SubtitleFormat,
    SubtitleListResponse,
    SubtitleResponse,
    SubtitleSettingsRequest,
    SubtitleSettingsResponse,
    SubtitleStatus,
    SubtitleUploadRequest,
)

router = APIRouter(prefix="/subtitles", tags=["subtitles"])

VIDEO_SUBTITLES: dict[str, list[dict]] = {}
USER_SUBTITLE_SETTINGS: dict[str, dict] = {}


def generate_dummy_cues(duration: float = 60.0) -> list[SubtitleCue]:
    """Генерирует демо-субтитры."""
    cues = [
        SubtitleCue(id=1, start_time=0.0, end_time=3.0, text="Привет! Это демонстрация субтитров."),
        SubtitleCue(id=2, start_time=3.5, end_time=6.0, text="Субтитры генерируются автоматически."),
        SubtitleCue(id=3, start_time=6.5, end_time=9.0, text="Вы можете настроить их отображение."),
        SubtitleCue(id=4, start_time=9.5, end_time=12.0, text="Размер шрифта, цвет, позицию..."),
        SubtitleCue(id=5, start_time=12.5, end_time=15.0, text="Спасибо за просмотр!"),
    ]
    return cues


@router.post("/generate", response_model=SubtitleResponse)
async def generate_subtitles(
    request: GenerateSubtitlesRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> SubtitleResponse:
    """Запустить генерацию субтитров для видео."""
    subtitle_id = uuid.uuid4()
    now = datetime.now(UTC)

    cues = generate_dummy_cues()

    subtitle = {
        "id": subtitle_id,
        "video_id": request.video_id,
        "language": request.language,
        "status": SubtitleStatus.COMPLETED,
        "format": SubtitleFormat.VTT,
        "cues": cues,
        "created_at": now,
    }

    video_key = str(request.video_id)
    if video_key not in VIDEO_SUBTITLES:
        VIDEO_SUBTITLES[video_key] = []
    VIDEO_SUBTITLES[video_key].append(subtitle)

    return SubtitleResponse(**subtitle)


@router.get("/video/{video_id}", response_model=SubtitleListResponse)
async def list_video_subtitles(
    video_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
) -> SubtitleListResponse:
    """Получить список субтитров для видео."""
    subtitles = VIDEO_SUBTITLES.get(str(video_id), [])

    return SubtitleListResponse(
        subtitles=[SubtitleResponse(**s) for s in subtitles],
        video_id=video_id,
    )


@router.get("/{subtitle_id}", response_model=SubtitleResponse)
async def get_subtitle(
    subtitle_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
) -> SubtitleResponse:
    """Получить субтитры по ID."""
    for video_subs in VIDEO_SUBTITLES.values():
        for sub in video_subs:
            if sub["id"] == subtitle_id:
                return SubtitleResponse(**sub)

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail={"message": "Субтитры не найдены", "code": "subtitle_not_found"},
    )


@router.post("/upload", response_model=SubtitleResponse)
async def upload_subtitles(
    request: SubtitleUploadRequest,
    current_user: User = Depends(get_current_user),
) -> SubtitleResponse:
    """Загрузить готовые субтитры."""
    subtitle_id = uuid.uuid4()
    now = datetime.now(UTC)

    cues = parse_subtitle_content(request.content, request.format)

    subtitle = {
        "id": subtitle_id,
        "video_id": request.video_id,
        "language": request.language,
        "status": SubtitleStatus.COMPLETED,
        "format": request.format,
        "cues": cues,
        "created_at": now,
    }

    video_key = str(request.video_id)
    if video_key not in VIDEO_SUBTITLES:
        VIDEO_SUBTITLES[video_key] = []
    VIDEO_SUBTITLES[video_key].append(subtitle)

    return SubtitleResponse(**subtitle)


def parse_subtitle_content(content: str, fmt: SubtitleFormat) -> list[SubtitleCue]:
    """Парсит содержимое субтитров."""
    cues = []
    lines = content.strip().split("\n")
    cue_id = 1

    i = 0
    while i < len(lines):
        line = lines[i].strip()

        if "-->" in line:
            times = line.split("-->")
            start = parse_time(times[0].strip())
            end = parse_time(times[1].strip().split()[0])

            text_lines = []
            i += 1
            while i < len(lines) and lines[i].strip() and "-->" not in lines[i]:
                text_lines.append(lines[i].strip())
                i += 1

            cues.append(SubtitleCue(
                id=cue_id,
                start_time=start,
                end_time=end,
                text=" ".join(text_lines),
            ))
            cue_id += 1
        else:
            i += 1

    return cues if cues else generate_dummy_cues()


def parse_time(time_str: str) -> float:
    """Парсит время из строки формата HH:MM:SS.mmm или MM:SS.mmm."""
    parts = time_str.replace(",", ".").split(":")
    if len(parts) == 3:
        hours, minutes, seconds = parts
        return float(hours) * 3600 + float(minutes) * 60 + float(seconds)
    elif len(parts) == 2:
        minutes, seconds = parts
        return float(minutes) * 60 + float(seconds)
    return 0.0


@router.delete("/{subtitle_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_subtitle(
    subtitle_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
) -> None:
    """Удалить субтитры."""
    for video_key, video_subs in VIDEO_SUBTITLES.items():
        for i, sub in enumerate(video_subs):
            if sub["id"] == subtitle_id:
                video_subs.pop(i)
                return

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail={"message": "Субтитры не найдены", "code": "subtitle_not_found"},
    )


@router.get("/settings", response_model=SubtitleSettingsResponse)
async def get_subtitle_settings(
    current_user: User = Depends(get_current_user),
) -> SubtitleSettingsResponse:
    """Получить настройки субтитров пользователя."""
    settings = USER_SUBTITLE_SETTINGS.get(str(current_user.id), {
        "enabled": True,
        "font_size": 16,
        "background_opacity": 0.7,
        "position": "bottom",
        "text_color": "#FFFFFF",
        "background_color": "#000000",
    })

    return SubtitleSettingsResponse(**settings)


@router.put("/settings", response_model=SubtitleSettingsResponse)
async def update_subtitle_settings(
    request: SubtitleSettingsRequest,
    current_user: User = Depends(get_current_user),
) -> SubtitleSettingsResponse:
    """Обновить настройки субтитров."""
    USER_SUBTITLE_SETTINGS[str(current_user.id)] = request.model_dump()

    return SubtitleSettingsResponse(**request.model_dump())
