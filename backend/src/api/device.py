"""API эндпоинты для мульти-устройств."""

import uuid
from datetime import UTC, datetime

from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.deps import get_current_user
from src.db import get_db
from src.models.user import User
from src.schemas.device import (
    DeviceListResponse,
    DevicePlatform,
    DeviceRegisterRequest,
    DeviceResponse,
    DeviceType,
    DeviceUpdateRequest,
    SessionResponse,
    TerminateSessionsRequest,
)

router = APIRouter(prefix="/devices", tags=["devices"])

USER_DEVICES: dict[str, list[dict]] = {}
CURRENT_DEVICE: dict[str, str] = {}


def detect_device_type(user_agent: str) -> DeviceType:
    """Определяет тип устройства по User-Agent."""
    ua = user_agent.lower()
    if "mobile" in ua or "android" in ua or "iphone" in ua:
        return DeviceType.MOBILE
    if "tablet" in ua or "ipad" in ua:
        return DeviceType.TABLET
    if "windows" in ua or "macintosh" in ua or "linux" in ua:
        return DeviceType.DESKTOP
    return DeviceType.WEB


def detect_platform(user_agent: str) -> DevicePlatform:
    """Определяет платформу по User-Agent."""
    ua = user_agent.lower()
    if "windows" in ua:
        return DevicePlatform.WINDOWS
    if "macintosh" in ua or "mac os" in ua:
        return DevicePlatform.MACOS
    if "linux" in ua and "android" not in ua:
        return DevicePlatform.LINUX
    if "android" in ua:
        return DevicePlatform.ANDROID
    if "iphone" in ua or "ipad" in ua:
        return DevicePlatform.IOS
    return DevicePlatform.WEB


@router.post("", response_model=DeviceResponse)
async def register_device(
    request_data: DeviceRegisterRequest,
    request: Request,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> DeviceResponse:
    """Зарегистрировать новое устройство."""
    user_id = str(current_user.id)
    device_id = uuid.uuid4()
    now = datetime.now(UTC)

    user_agent = request.headers.get("user-agent", "")
    client_ip = request.client.host if request.client else None

    device = {
        "id": device_id,
        "user_id": current_user.id,
        "device_name": request_data.device_name,
        "device_type": request_data.device_type or detect_device_type(user_agent),
        "platform": request_data.platform or detect_platform(user_agent),
        "is_current": True,
        "last_active_at": now,
        "ip_address": client_ip,
        "location": None,
        "push_token": request_data.push_token,
        "created_at": now,
    }

    if user_id not in USER_DEVICES:
        USER_DEVICES[user_id] = []

    for d in USER_DEVICES[user_id]:
        d["is_current"] = False

    USER_DEVICES[user_id].append(device)
    CURRENT_DEVICE[user_id] = str(device_id)

    return DeviceResponse(**device)


@router.get("", response_model=DeviceListResponse)
async def list_devices(
    current_user: User = Depends(get_current_user),
) -> DeviceListResponse:
    """Получить список устройств пользователя."""
    user_id = str(current_user.id)
    devices = USER_DEVICES.get(user_id, [])
    current_id = CURRENT_DEVICE.get(user_id)

    return DeviceListResponse(
        devices=[DeviceResponse(**d) for d in devices],
        current_device_id=uuid.UUID(current_id) if current_id else None,
    )


@router.get("/{device_id}", response_model=DeviceResponse)
async def get_device(
    device_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
) -> DeviceResponse:
    """Получить информацию об устройстве."""
    user_id = str(current_user.id)
    devices = USER_DEVICES.get(user_id, [])

    device = next((d for d in devices if d["id"] == device_id), None)
    if not device:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"message": "Устройство не найдено", "code": "device_not_found"},
        )

    return DeviceResponse(**device)


@router.put("/{device_id}", response_model=DeviceResponse)
async def update_device(
    device_id: uuid.UUID,
    request_data: DeviceUpdateRequest,
    current_user: User = Depends(get_current_user),
) -> DeviceResponse:
    """Обновить информацию об устройстве."""
    user_id = str(current_user.id)
    devices = USER_DEVICES.get(user_id, [])

    device = next((d for d in devices if d["id"] == device_id), None)
    if not device:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"message": "Устройство не найдено", "code": "device_not_found"},
        )

    if request_data.device_name is not None:
        device["device_name"] = request_data.device_name
    if request_data.push_token is not None:
        device["push_token"] = request_data.push_token

    return DeviceResponse(**device)


@router.delete("/{device_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_device(
    device_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
) -> None:
    """Удалить устройство (завершить сессию)."""
    user_id = str(current_user.id)
    devices = USER_DEVICES.get(user_id, [])

    device_idx = next((i for i, d in enumerate(devices) if d["id"] == device_id), None)
    if device_idx is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"message": "Устройство не найдено", "code": "device_not_found"},
        )

    devices.pop(device_idx)


@router.get("/sessions/active", response_model=list[SessionResponse])
async def list_active_sessions(
    current_user: User = Depends(get_current_user),
) -> list[SessionResponse]:
    """Получить список активных сессий."""
    user_id = str(current_user.id)
    devices = USER_DEVICES.get(user_id, [])

    return [
        SessionResponse(
            device_id=d["id"],
            device_name=d["device_name"],
            device_type=d["device_type"],
            platform=d["platform"],
            is_current=d["is_current"],
            last_active_at=d["last_active_at"],
            ip_address=d.get("ip_address"),
            location=d.get("location"),
        )
        for d in devices
    ]


@router.post("/sessions/terminate", status_code=status.HTTP_204_NO_CONTENT)
async def terminate_sessions(
    request_data: TerminateSessionsRequest,
    current_user: User = Depends(get_current_user),
) -> None:
    """Завершить сессии на устройствах."""
    user_id = str(current_user.id)
    current_id = CURRENT_DEVICE.get(user_id)

    if request_data.terminate_all_except_current:
        USER_DEVICES[user_id] = [
            d for d in USER_DEVICES.get(user_id, [])
            if str(d["id"]) == current_id
        ]
    elif request_data.device_ids:
        USER_DEVICES[user_id] = [
            d for d in USER_DEVICES.get(user_id, [])
            if d["id"] not in request_data.device_ids
        ]
