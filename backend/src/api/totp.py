"""API эндпоинты для 2FA [SECURITY]."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.deps import get_current_user
from src.db import get_db
from src.models.user import User
from src.schemas.totp import (
    Setup2FAResponse,
    TwoFactorStatusResponse,
    Verify2FARequest,
    Verify2FAResponse,
)
from src.services.totp import TOTPService

router = APIRouter(prefix="/2fa", tags=["2fa"])


@router.get("/status", response_model=TwoFactorStatusResponse)
async def get_2fa_status(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> TwoFactorStatusResponse:
    """Получить статус 2FA."""
    service = TOTPService(db)
    enabled = await service.is_2fa_enabled(current_user.id)
    return TwoFactorStatusResponse(enabled=enabled)


@router.post("/setup", response_model=Setup2FAResponse)
async def setup_2fa(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> Setup2FAResponse:
    """Настроить 2FA (шаг 1: получить секрет и QR-код)."""
    service = TOTPService(db)

    try:
        result = await service.setup_2fa(current_user.id)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"message": str(e), "code": "setup_error"},
        ) from e

    return Setup2FAResponse(
        secret=result["secret"],
        provisioning_uri=result["provisioning_uri"],
        qr_code=result["qr_code"],
    )


@router.post("/verify", response_model=Verify2FAResponse)
async def verify_and_enable_2fa(
    data: Verify2FARequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> Verify2FAResponse:
    """Подтвердить и включить 2FA (шаг 2: ввести код из аутентификатора)."""
    service = TOTPService(db)

    try:
        success = await service.verify_and_enable_2fa(current_user.id, data.code)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"message": str(e), "code": "verify_error"},
        ) from e

    if not success:
        return Verify2FAResponse(success=False, message="Неверный код")

    return Verify2FAResponse(success=True, message="2FA успешно включена")


@router.post("/disable", response_model=Verify2FAResponse)
async def disable_2fa(
    data: Verify2FARequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> Verify2FAResponse:
    """Отключить 2FA."""
    service = TOTPService(db)

    try:
        success = await service.disable_2fa(current_user.id, data.code)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"message": str(e), "code": "disable_error"},
        ) from e

    if not success:
        return Verify2FAResponse(success=False, message="Неверный код")

    return Verify2FAResponse(success=True, message="2FA успешно отключена")
