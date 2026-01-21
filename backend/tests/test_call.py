"""Тесты аудио/видео звонков."""

import uuid
from datetime import UTC, datetime

from src.models.call import CallStatus, CallType


class TestCallModels:
    """Тесты моделей звонков."""

    def test_call_type_values(self):
        """Проверка значений типов звонка."""
        assert CallType.AUDIO.value == "audio"
        assert CallType.VIDEO.value == "video"

    def test_call_status_values(self):
        """Проверка значений статусов звонка."""
        assert CallStatus.PENDING.value == "pending"
        assert CallStatus.RINGING.value == "ringing"
        assert CallStatus.ACTIVE.value == "active"
        assert CallStatus.ENDED.value == "ended"
        assert CallStatus.MISSED.value == "missed"
        assert CallStatus.DECLINED.value == "declined"
        assert CallStatus.FAILED.value == "failed"


class TestCallSchemas:
    """Тесты схем звонков."""

    def test_initiate_call_request(self):
        """InitiateCallRequest валидация."""
        from src.schemas.call import InitiateCallRequest

        callee_id = uuid.uuid4()
        data = InitiateCallRequest(callee_id=callee_id, call_type="video")
        assert data.callee_id == callee_id
        assert data.call_type == "video"

    def test_initiate_call_request_default_type(self):
        """InitiateCallRequest с типом по умолчанию."""
        from src.schemas.call import InitiateCallRequest

        callee_id = uuid.uuid4()
        data = InitiateCallRequest(callee_id=callee_id)
        assert data.call_type == "audio"

    def test_call_response(self):
        """CallResponse валидация."""
        from src.schemas.call import CallResponse

        now = datetime.now(UTC)
        data = CallResponse(
            id=uuid.uuid4(),
            caller_id=uuid.uuid4(),
            caller_name="Иван",
            callee_id=uuid.uuid4(),
            callee_name="Мария",
            call_type="audio",
            status="active",
            started_at=now,
            ended_at=None,
            duration_seconds=None,
            created_at=now,
        )
        assert data.status == "active"
        assert data.caller_name == "Иван"

    def test_call_action_request(self):
        """CallActionRequest валидация."""
        from src.schemas.call import CallActionRequest

        data = CallActionRequest(action="accept")
        assert data.action == "accept"

    def test_webrtc_signal_request(self):
        """WebRTCSignalRequest валидация."""
        from src.schemas.call import WebRTCSignalRequest

        data = WebRTCSignalRequest(
            call_id=uuid.uuid4(),
            signal_type="offer",
            payload={"sdp": "v=0..."},
        )
        assert data.signal_type == "offer"

    def test_call_history_response(self):
        """CallHistoryResponse валидация."""
        from src.schemas.call import CallHistoryResponse

        data = CallHistoryResponse(calls=[], total=0)
        assert data.total == 0
