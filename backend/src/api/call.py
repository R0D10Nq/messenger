"""API эндпоинты для аудио/видео звонков."""

import uuid

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.deps import get_current_user
from src.db import get_db
from src.models.call import Call
from src.models.user import User
from src.schemas.call import (
    CallActionRequest,
    CallHistoryResponse,
    CallResponse,
    InitiateCallRequest,
)
from src.services.call import CallService

router = APIRouter(prefix="/calls", tags=["calls"])


async def _build_call_response(call: Call, db: AsyncSession) -> CallResponse:
    """Построить ответ звонка."""
    caller = await db.get(User, call.caller_id)
    callee = await db.get(User, call.callee_id)

    return CallResponse(
        id=call.id,
        caller_id=call.caller_id,
        caller_name=caller.name if caller else "Удалённый пользователь",
        callee_id=call.callee_id,
        callee_name=callee.name if callee else "Удалённый пользователь",
        call_type=call.call_type,
        status=call.status,
        started_at=call.started_at,
        ended_at=call.ended_at,
        duration_seconds=call.duration_seconds,
        created_at=call.created_at,
    )


@router.post("", response_model=CallResponse, status_code=status.HTTP_201_CREATED)
async def initiate_call(
    data: InitiateCallRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> CallResponse:
    """Инициировать звонок."""
    service = CallService(db)

    try:
        call = await service.initiate_call(
            caller_id=current_user.id,
            callee_id=data.callee_id,
            call_type=data.call_type,
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"message": str(e), "code": "call_error"},
        ) from e

    return await _build_call_response(call, db)


@router.get("/{call_id}", response_model=CallResponse)
async def get_call(
    call_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> CallResponse:
    """Получить информацию о звонке."""
    service = CallService(db)
    call = await service.get_call(call_id)

    if not call:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"message": "Звонок не найден", "code": "not_found"},
        )

    if call.caller_id != current_user.id and call.callee_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={"message": "Нет доступа к звонку", "code": "forbidden"},
        )

    return await _build_call_response(call, db)


@router.post("/{call_id}/action", response_model=CallResponse)
async def call_action(
    call_id: uuid.UUID,
    data: CallActionRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> CallResponse:
    """Выполнить действие со звонком (accept/decline/end)."""
    service = CallService(db)

    try:
        if data.action == "accept":
            call = await service.accept_call(call_id, current_user.id)
        elif data.action == "decline":
            call = await service.decline_call(call_id, current_user.id)
        elif data.action == "end":
            call = await service.end_call(call_id, current_user.id)
        else:
            raise ValueError("Неизвестное действие")
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"message": str(e), "code": "action_error"},
        ) from e

    return await _build_call_response(call, db)


@router.get("", response_model=CallHistoryResponse)
async def get_call_history(
    limit: int = Query(50, ge=1, le=100),
    offset: int = Query(0, ge=0),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> CallHistoryResponse:
    """Получить историю звонков."""
    service = CallService(db)
    calls, total = await service.get_call_history(current_user.id, limit, offset)

    calls_response = [await _build_call_response(call, db) for call in calls]

    return CallHistoryResponse(calls=calls_response, total=total)
