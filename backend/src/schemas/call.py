"""Схемы для аудио/видео звонков."""

import uuid
from datetime import datetime

from pydantic import BaseModel, Field


class InitiateCallRequest(BaseModel):
    """Запрос на инициацию звонка."""

    callee_id: uuid.UUID
    call_type: str = Field(pattern="^(audio|video)$", default="audio")


class CallResponse(BaseModel):
    """Ответ с данными звонка."""

    id: uuid.UUID
    caller_id: uuid.UUID
    caller_name: str
    callee_id: uuid.UUID
    callee_name: str
    call_type: str
    status: str
    started_at: datetime | None
    ended_at: datetime | None
    duration_seconds: int | None
    created_at: datetime

    model_config = {"from_attributes": True}


class CallActionRequest(BaseModel):
    """Запрос на действие со звонком."""

    action: str = Field(pattern="^(accept|decline|end)$")


class WebRTCSignalRequest(BaseModel):
    """WebRTC сигнальное сообщение."""

    call_id: uuid.UUID
    signal_type: str = Field(pattern="^(offer|answer|ice-candidate)$")
    payload: dict[str, object]


class CallHistoryResponse(BaseModel):
    """История звонков."""

    calls: list[CallResponse]
    total: int
