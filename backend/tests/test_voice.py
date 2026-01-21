"""Тесты для голосовых сообщений."""

import uuid

import pytest


class TestVoiceSchemas:
    """Тесты схем голосовых сообщений."""

    def test_voice_message_create(self):
        """VoiceMessageCreate валидация."""
        from src.schemas.voice import VoiceMessageCreate

        data = VoiceMessageCreate(
            chat_id=uuid.uuid4(),
            duration=30,
            waveform=[10, 20, 30, 40, 50],
        )
        assert data.duration == 30
        assert len(data.waveform) == 5

    def test_voice_message_create_min_duration(self):
        """Минимальная длительность 1 секунда."""
        from src.schemas.voice import VoiceMessageCreate

        data = VoiceMessageCreate(chat_id=uuid.uuid4(), duration=1)
        assert data.duration == 1

    def test_voice_message_create_max_duration(self):
        """Максимальная длительность 600 секунд."""
        from src.schemas.voice import VoiceMessageCreate

        data = VoiceMessageCreate(chat_id=uuid.uuid4(), duration=600)
        assert data.duration == 600

    def test_voice_message_create_invalid_duration(self):
        """Некорректная длительность вызывает ошибку."""
        from pydantic import ValidationError

        from src.schemas.voice import VoiceMessageCreate

        with pytest.raises(ValidationError):
            VoiceMessageCreate(chat_id=uuid.uuid4(), duration=0)

        with pytest.raises(ValidationError):
            VoiceMessageCreate(chat_id=uuid.uuid4(), duration=601)

    def test_voice_message_create_without_waveform(self):
        """VoiceMessageCreate без waveform."""
        from src.schemas.voice import VoiceMessageCreate

        data = VoiceMessageCreate(chat_id=uuid.uuid4(), duration=10)
        assert data.waveform is None

    def test_voice_message_response(self):
        """VoiceMessageResponse валидация."""
        from datetime import UTC, datetime

        from src.schemas.voice import VoiceMessageResponse

        now = datetime.now(UTC)
        data = VoiceMessageResponse(
            id=uuid.uuid4(),
            message_id=uuid.uuid4(),
            chat_id=uuid.uuid4(),
            sender_id=uuid.uuid4(),
            file_url="https://example.com/voice.ogg",
            duration=45,
            waveform=[10, 20, 30],
            is_listened=False,
            created_at=now,
        )
        assert data.duration == 45
        assert data.is_listened is False

    def test_voice_transcription_response(self):
        """VoiceTranscriptionResponse валидация."""
        from src.schemas.voice import VoiceTranscriptionResponse

        data = VoiceTranscriptionResponse(
            message_id=uuid.uuid4(),
            text="Привет, как дела?",
            language="ru",
            confidence=0.95,
        )
        assert data.text == "Привет, как дела?"
        assert data.language == "ru"
        assert data.confidence == 0.95

    def test_voice_transcription_response_no_confidence(self):
        """VoiceTranscriptionResponse без confidence."""
        from src.schemas.voice import VoiceTranscriptionResponse

        data = VoiceTranscriptionResponse(
            message_id=uuid.uuid4(),
            text="Тестовый текст",
            language=None,
            confidence=None,
        )
        assert data.confidence is None
        assert data.language is None
