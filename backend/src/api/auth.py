"""API эндпоинты аутентификации [SECURITY]."""

from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.db import get_db
from src.schemas.auth import (
    LoginRequest,
    RefreshTokenRequest,
    RegisterRequest,
    TokenResponse,
    UserResponse,
)
from src.services.auth import AuthError, AuthService

router = APIRouter(prefix="/auth", tags=["auth"])


def get_client_info(request: Request) -> tuple[str | None, str | None]:
    """Извлечь информацию о клиенте из запроса."""
    device_info = request.headers.get("User-Agent")
    ip_address = request.client.host if request.client else None
    forwarded = request.headers.get("X-Forwarded-For")
    if forwarded:
        ip_address = forwarded.split(",")[0].strip()
    return device_info, ip_address


@router.post("/register", response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
async def register(
    data: RegisterRequest,
    request: Request,
    db: AsyncSession = Depends(get_db),
) -> TokenResponse:
    """Регистрация нового пользователя с автоматическим входом."""
    service = AuthService(db)
    device_info, ip_address = get_client_info(request)
    
    try:
        user = await service.register(
            email=data.email,
            password=data.password,
            name=data.name,
        )
        # Автоматический вход после регистрации
        _, access_token, refresh_token = await service.login(
            email=data.email,
            password=data.password,
            device_info=device_info,
            ip_address=ip_address,
        )
        return TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token,
        )
    except AuthError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"message": e.message, "code": e.code},
        ) from e


@router.post("/login", response_model=TokenResponse)
async def login(
    data: LoginRequest,
    request: Request,
    db: AsyncSession = Depends(get_db),
) -> TokenResponse:
    """Вход в систему."""
    service = AuthService(db)
    device_info, ip_address = get_client_info(request)

    try:
        _, access_token, refresh_token = await service.login(
            email=data.email,
            password=data.password,
            device_info=device_info,
            ip_address=ip_address,
        )
        return TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token,
        )
    except AuthError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"message": e.message, "code": e.code},
        ) from e


@router.post("/refresh", response_model=TokenResponse)
async def refresh_tokens(
    data: RefreshTokenRequest,
    request: Request,
    db: AsyncSession = Depends(get_db),
) -> TokenResponse:
    """Обновление токенов."""
    service = AuthService(db)
    device_info, ip_address = get_client_info(request)

    try:
        access_token, refresh_token = await service.refresh_tokens(
            refresh_token=data.refresh_token,
            device_info=device_info,
            ip_address=ip_address,
        )
        return TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token,
        )
    except AuthError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"message": e.message, "code": e.code},
        ) from e


@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
async def logout(
    data: RefreshTokenRequest,
    db: AsyncSession = Depends(get_db),
) -> None:
    """Выход из системы."""
    service = AuthService(db)
    await service.logout(data.refresh_token)
