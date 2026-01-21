"""Зависимости для API [SECURITY]."""

import uuid

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession

from src.db import get_db
from src.models.user import User
from src.services.auth import AuthService

security = HTTPBearer()


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: AsyncSession = Depends(get_db),
) -> User:
    """Получить текущего авторизованного пользователя."""
    token = credentials.credentials
    service = AuthService(db)

    user_id = service.verify_access_token(token)
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"message": "Невалидный или истёкший токен", "code": "invalid_token"},
            headers={"WWW-Authenticate": "Bearer"},
        )

    user = await service.get_user_by_id(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"message": "Пользователь не найден", "code": "user_not_found"},
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={"message": "Аккаунт деактивирован", "code": "account_inactive"},
        )

    return user


async def get_current_user_id(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: AsyncSession = Depends(get_db),
) -> uuid.UUID:
    """Получить ID текущего пользователя (легковесная версия без загрузки User)."""
    token = credentials.credentials
    service = AuthService(db)

    user_id = service.verify_access_token(token)
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"message": "Невалидный или истёкший токен", "code": "invalid_token"},
            headers={"WWW-Authenticate": "Bearer"},
        )

    return user_id
