"""API эндпоинты для E2E шифрования [SECURITY]."""

import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.deps import get_current_user
from src.db import get_db
from src.models.user import User
from src.schemas.encryption import (
    KeyBundleResponse,
    PrekeysCountResponse,
    PublicKeyResponse,
    RegisterKeysRequest,
    UploadPrekeysRequest,
)
from src.services.encryption import EncryptionService

router = APIRouter(prefix="/encryption", tags=["encryption"])


@router.post("/keys", response_model=PublicKeyResponse, status_code=status.HTTP_201_CREATED)
async def register_keys(
    data: RegisterKeysRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> PublicKeyResponse:
    """Зарегистрировать ключи устройства."""
    service = EncryptionService(db)

    public_key = await service.register_keys(
        user_id=current_user.id,
        device_id=data.device_id,
        identity_key=data.identity_key,
        signed_prekey=data.signed_prekey,
        signed_prekey_signature=data.signed_prekey_signature,
        one_time_prekeys=data.one_time_prekeys,
    )

    return PublicKeyResponse(
        id=public_key.id,
        user_id=public_key.user_id,
        device_id=public_key.device_id,
        identity_key=public_key.identity_key,
        signed_prekey=public_key.signed_prekey,
        signed_prekey_signature=public_key.signed_prekey_signature,
        created_at=public_key.created_at,
    )


@router.get("/keys/{user_id}", response_model=KeyBundleResponse)
async def get_key_bundle(
    user_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> KeyBundleResponse:
    """Получить пакет ключей пользователя для установки сессии."""
    service = EncryptionService(db)

    bundle = await service.get_key_bundle(user_id)
    if not bundle:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"message": "Ключи пользователя не найдены", "code": "keys_not_found"},
        )

    return KeyBundleResponse(
        identity_key=bundle["identity_key"] or "",
        signed_prekey=bundle["signed_prekey"] or "",
        signed_prekey_signature=bundle["signed_prekey_signature"] or "",
        one_time_prekey=bundle["one_time_prekey"],
    )


@router.post("/prekeys", response_model=PrekeysCountResponse)
async def upload_prekeys(
    data: UploadPrekeysRequest,
    device_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> PrekeysCountResponse:
    """Загрузить дополнительные one-time prekeys."""
    service = EncryptionService(db)

    try:
        await service.upload_prekeys(current_user.id, device_id, data.prekeys)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"message": str(e), "code": "upload_error"},
        ) from e

    count = await service.get_prekeys_count(current_user.id, device_id)

    return PrekeysCountResponse(count=count, device_id=device_id)


@router.get("/prekeys/count", response_model=PrekeysCountResponse)
async def get_prekeys_count(
    device_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> PrekeysCountResponse:
    """Получить количество доступных prekeys."""
    service = EncryptionService(db)

    count = await service.get_prekeys_count(current_user.id, device_id)

    return PrekeysCountResponse(count=count, device_id=device_id)
