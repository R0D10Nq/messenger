"""Тесты транскрипции голосовых сообщений."""

import uuid
from datetime import UTC, datetime

from src.models.media import TranscriptionStatus


class TestTranscriptionModels:
    """Тесты моделей транскрипции."""

    def test_transcription_status_values(self):
        """Проверка значений статусов транскрипции."""
        assert TranscriptionStatus.PENDING.value == "pending"
        assert TranscriptionStatus.PROCESSING.value == "processing"
        assert TranscriptionStatus.COMPLETED.value == "completed"
        assert TranscriptionStatus.FAILED.value == "failed"


class TestTranscriptionSchemas:
    """Тесты схем транскрипции."""

    def test_transcription_response(self):
        """TranscriptionResponse валидация."""
        from src.schemas.media import TranscriptionResponse

        now = datetime.now(UTC)
        data = TranscriptionResponse(
            id=uuid.uuid4(),
            media_id=uuid.uuid4(),
            status="completed",
            text="Привет, это тестовое сообщение.",
            language="ru",
            duration_seconds=5.5,
            error_message=None,
            created_at=now,
            completed_at=now,
        )
        assert data.status == "completed"
        assert data.text == "Привет, это тестовое сообщение."
        assert data.language == "ru"

    def test_transcription_response_pending(self):
        """TranscriptionResponse для pending статуса."""
        from src.schemas.media import TranscriptionResponse

        now = datetime.now(UTC)
        data = TranscriptionResponse(
            id=uuid.uuid4(),
            media_id=uuid.uuid4(),
            status="pending",
            text=None,
            language=None,
            duration_seconds=10.0,
            error_message=None,
            created_at=now,
            completed_at=None,
        )
        assert data.status == "pending"
        assert data.text is None
        assert data.completed_at is None

    def test_transcription_response_failed(self):
        """TranscriptionResponse для failed статуса."""
        from src.schemas.media import TranscriptionResponse

        now = datetime.now(UTC)
        data = TranscriptionResponse(
            id=uuid.uuid4(),
            media_id=uuid.uuid4(),
            status="failed",
            text=None,
            language=None,
            duration_seconds=15.0,
            error_message="Не удалось распознать речь",
            created_at=now,
            completed_at=now,
        )
        assert data.status == "failed"
        assert data.error_message == "Не удалось распознать речь"

    def test_create_transcription_request(self):
        """CreateTranscriptionRequest валидация."""
        from src.schemas.media import CreateTranscriptionRequest

        media_id = uuid.uuid4()
        data = CreateTranscriptionRequest(media_id=media_id)
        assert data.media_id == media_id
