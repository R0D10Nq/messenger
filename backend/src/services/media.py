"""Сервис для работы с медиафайлами."""

import mimetypes
import uuid
from pathlib import Path

from src.config import get_settings
from src.models.media import MediaType

ALLOWED_IMAGE_TYPES = {"image/jpeg", "image/png", "image/gif", "image/webp"}
ALLOWED_VIDEO_TYPES = {"video/mp4", "video/webm", "video/quicktime"}
ALLOWED_AUDIO_TYPES = {"audio/mpeg", "audio/ogg", "audio/wav", "audio/webm"}
ALLOWED_FILE_TYPES = {
    "application/pdf",
    "application/zip",
    "application/x-zip-compressed",
    "text/plain",
    "application/msword",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
}

MAX_FILE_SIZE = 100 * 1024 * 1024  # 100MB
MAX_IMAGE_SIZE = 10 * 1024 * 1024  # 10MB
MAX_VOICE_SIZE = 20 * 1024 * 1024  # 20MB


def get_media_type(mime_type: str, is_voice: bool = False) -> MediaType:
    """Определить тип медиа по MIME-типу."""
    if is_voice:
        return MediaType.VOICE
    if mime_type in ALLOWED_IMAGE_TYPES:
        return MediaType.IMAGE
    if mime_type in ALLOWED_VIDEO_TYPES:
        return MediaType.VIDEO
    if mime_type in ALLOWED_AUDIO_TYPES:
        return MediaType.AUDIO
    return MediaType.FILE


def is_allowed_file(mime_type: str) -> bool:
    """Проверить, разрешён ли тип файла."""
    all_allowed = (
        ALLOWED_IMAGE_TYPES
        | ALLOWED_VIDEO_TYPES
        | ALLOWED_AUDIO_TYPES
        | ALLOWED_FILE_TYPES
    )
    return mime_type in all_allowed


def get_max_size(media_type: MediaType) -> int:
    """Получить максимальный размер для типа медиа."""
    if media_type == MediaType.IMAGE:
        return MAX_IMAGE_SIZE
    if media_type == MediaType.VOICE:
        return MAX_VOICE_SIZE
    return MAX_FILE_SIZE


def generate_storage_path(
    user_id: uuid.UUID,
    media_type: MediaType,
    original_filename: str,
) -> tuple[str, str]:
    """Сгенерировать путь для хранения файла."""
    settings = get_settings()
    ext = Path(original_filename).suffix.lower()
    file_id = uuid.uuid4()
    filename = f"{file_id}{ext}"

    type_folder = media_type.value
    path = Path(settings.media_storage_path) / str(user_id) / type_folder
    path.mkdir(parents=True, exist_ok=True)

    storage_path = str(path / filename)
    return filename, storage_path


def get_file_url(storage_path: str) -> str:
    """Получить URL для доступа к файлу."""
    settings = get_settings()
    relative_path = storage_path.replace(settings.media_storage_path, "").lstrip("/\\")
    return f"/media/{relative_path}"


def guess_mime_type(filename: str) -> str:
    """Определить MIME-тип по имени файла."""
    mime_type, _ = mimetypes.guess_type(filename)
    return mime_type or "application/octet-stream"


def validate_file_size(size: int, media_type: MediaType) -> bool:
    """Проверить размер файла."""
    max_size = get_max_size(media_type)
    return size <= max_size
