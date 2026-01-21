"""Схемы для субтитров видео."""

import uuid
from datetime import datetime
from enum import Enum

from pydantic import BaseModel, Field


class SubtitleFormat(str, Enum):
    """Формат субтитров."""

    SRT = "srt"
    VTT = "vtt"
    ASS = "ass"


class SubtitleStatus(str, Enum):
    """Статус генерации субтитров."""

    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"


class SubtitleCue(BaseModel):
    """Отдельная реплика субтитров."""

    id: int
    start_time: float
    end_time: float
    text: str


class GenerateSubtitlesRequest(BaseModel):
    """Запрос на генерацию субтитров."""

    video_id: uuid.UUID
    language: str = "ru"
    auto_detect: bool = True


class SubtitleResponse(BaseModel):
    """Ответ с информацией о субтитрах."""

    id: uuid.UUID
    video_id: uuid.UUID
    language: str
    status: SubtitleStatus
    format: SubtitleFormat
    cues: list[SubtitleCue] | None
    created_at: datetime

    model_config = {"from_attributes": True}


class SubtitleListResponse(BaseModel):
    """Список субтитров для видео."""

    subtitles: list[SubtitleResponse]
    video_id: uuid.UUID


class SubtitleUploadRequest(BaseModel):
    """Запрос на загрузку субтитров."""

    video_id: uuid.UUID
    language: str
    content: str
    format: SubtitleFormat = SubtitleFormat.VTT


class SubtitleSettingsRequest(BaseModel):
    """Настройки отображения субтитров."""

    enabled: bool = True
    font_size: int = Field(16, ge=10, le=32)
    background_opacity: float = Field(0.7, ge=0, le=1)
    position: str = "bottom"
    text_color: str = "#FFFFFF"
    background_color: str = "#000000"


class SubtitleSettingsResponse(BaseModel):
    """Текущие настройки субтитров."""

    enabled: bool
    font_size: int
    background_opacity: float
    position: str
    text_color: str
    background_color: str
