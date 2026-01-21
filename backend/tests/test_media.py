"""Тесты медиафайлов."""

import uuid
from datetime import UTC, datetime

from src.models.media import MediaType
from src.services.media import (
    MAX_FILE_SIZE,
    MAX_IMAGE_SIZE,
    MAX_VOICE_SIZE,
    get_media_type,
    is_allowed_file,
    validate_file_size,
)


class TestMediaModels:
    """Тесты моделей медиа."""

    def test_media_type_values(self):
        """Проверка значений типов медиа."""
        assert MediaType.IMAGE.value == "image"
        assert MediaType.VIDEO.value == "video"
        assert MediaType.AUDIO.value == "audio"
        assert MediaType.VOICE.value == "voice"
        assert MediaType.FILE.value == "file"


class TestMediaService:
    """Тесты сервиса медиа."""

    def test_get_media_type_image(self):
        """Определение типа изображения."""
        assert get_media_type("image/jpeg") == MediaType.IMAGE
        assert get_media_type("image/png") == MediaType.IMAGE
        assert get_media_type("image/gif") == MediaType.IMAGE

    def test_get_media_type_video(self):
        """Определение типа видео."""
        assert get_media_type("video/mp4") == MediaType.VIDEO
        assert get_media_type("video/webm") == MediaType.VIDEO

    def test_get_media_type_audio(self):
        """Определение типа аудио."""
        assert get_media_type("audio/mpeg") == MediaType.AUDIO
        assert get_media_type("audio/ogg") == MediaType.AUDIO

    def test_get_media_type_voice(self):
        """Определение типа голосового сообщения."""
        assert get_media_type("audio/webm", is_voice=True) == MediaType.VOICE

    def test_get_media_type_file(self):
        """Определение типа файла."""
        assert get_media_type("application/pdf") == MediaType.FILE
        assert get_media_type("application/zip") == MediaType.FILE

    def test_is_allowed_file_true(self):
        """Разрешённые типы файлов."""
        assert is_allowed_file("image/jpeg") is True
        assert is_allowed_file("video/mp4") is True
        assert is_allowed_file("audio/mpeg") is True
        assert is_allowed_file("application/pdf") is True

    def test_is_allowed_file_false(self):
        """Запрещённые типы файлов."""
        assert is_allowed_file("application/x-executable") is False
        assert is_allowed_file("text/html") is False

    def test_validate_file_size_image(self):
        """Валидация размера изображения."""
        assert validate_file_size(1024 * 1024, MediaType.IMAGE) is True
        assert validate_file_size(MAX_IMAGE_SIZE, MediaType.IMAGE) is True
        assert validate_file_size(MAX_IMAGE_SIZE + 1, MediaType.IMAGE) is False

    def test_validate_file_size_voice(self):
        """Валидация размера голосового сообщения."""
        assert validate_file_size(1024 * 1024, MediaType.VOICE) is True
        assert validate_file_size(MAX_VOICE_SIZE, MediaType.VOICE) is True
        assert validate_file_size(MAX_VOICE_SIZE + 1, MediaType.VOICE) is False

    def test_validate_file_size_file(self):
        """Валидация размера файла."""
        assert validate_file_size(50 * 1024 * 1024, MediaType.FILE) is True
        assert validate_file_size(MAX_FILE_SIZE, MediaType.FILE) is True
        assert validate_file_size(MAX_FILE_SIZE + 1, MediaType.FILE) is False


class TestMediaSchemas:
    """Тесты схем медиа."""

    def test_media_file_response(self):
        """MediaFileResponse валидация."""
        from src.schemas.media import MediaFileResponse

        now = datetime.now(UTC)
        data = MediaFileResponse(
            id=uuid.uuid4(),
            media_type="image",
            filename="test.jpg",
            original_filename="photo.jpg",
            mime_type="image/jpeg",
            file_size=1024,
            url="/media/user/image/test.jpg",
            thumbnail_url=None,
            duration_seconds=None,
            width=800,
            height=600,
            created_at=now,
        )
        assert data.media_type == "image"
        assert data.file_size == 1024

    def test_upload_response(self):
        """UploadResponse валидация."""
        from src.schemas.media import MediaFileResponse, UploadResponse

        now = datetime.now(UTC)
        media = MediaFileResponse(
            id=uuid.uuid4(),
            media_type="image",
            filename="test.jpg",
            original_filename="photo.jpg",
            mime_type="image/jpeg",
            file_size=1024,
            url="/media/user/image/test.jpg",
            thumbnail_url=None,
            duration_seconds=None,
            width=None,
            height=None,
            created_at=now,
        )
        data = UploadResponse(media=media, message="Файл загружен")
        assert data.message == "Файл загружен"
