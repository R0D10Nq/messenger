"""Сервис E2E шифрования [SECURITY]."""

import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.encryption import OneTimePrekey, UserPublicKey


class EncryptionService:
    """Сервис для управления ключами E2E шифрования."""

    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def register_keys(
        self,
        user_id: uuid.UUID,
        device_id: str,
        identity_key: str,
        signed_prekey: str,
        signed_prekey_signature: str,
        one_time_prekeys: list[str],
    ) -> UserPublicKey:
        """Зарегистрировать ключи устройства."""
        existing = await self.db.execute(
            select(UserPublicKey)
            .where(UserPublicKey.user_id == user_id)
            .where(UserPublicKey.device_id == device_id)
        )
        old_key = existing.scalar_one_or_none()
        if old_key:
            old_key.is_active = False

        public_key = UserPublicKey(
            user_id=user_id,
            device_id=device_id,
            identity_key=identity_key,
            signed_prekey=signed_prekey,
            signed_prekey_signature=signed_prekey_signature,
        )
        self.db.add(public_key)
        await self.db.flush()

        for idx, prekey in enumerate(one_time_prekeys):
            otp = OneTimePrekey(
                user_public_key_id=public_key.id,
                key_id=idx,
                prekey=prekey,
            )
            self.db.add(otp)

        await self.db.flush()
        await self.db.refresh(public_key)

        return public_key

    async def get_user_public_key(
        self,
        user_id: uuid.UUID,
        device_id: str | None = None,
    ) -> UserPublicKey | None:
        """Получить активный публичный ключ пользователя."""
        query = select(UserPublicKey).where(
            UserPublicKey.user_id == user_id,
            UserPublicKey.is_active == True,  # noqa: E712
        )
        if device_id:
            query = query.where(UserPublicKey.device_id == device_id)

        result = await self.db.execute(query.order_by(UserPublicKey.created_at.desc()).limit(1))
        return result.scalar_one_or_none()

    async def get_key_bundle(
        self,
        user_id: uuid.UUID,
    ) -> dict[str, str | None] | None:
        """Получить пакет ключей для установки сессии."""
        public_key = await self.get_user_public_key(user_id)
        if not public_key:
            return None

        otp_result = await self.db.execute(
            select(OneTimePrekey)
            .where(OneTimePrekey.user_public_key_id == public_key.id)
            .where(OneTimePrekey.used == False)  # noqa: E712
            .order_by(OneTimePrekey.key_id)
            .limit(1)
        )
        one_time_prekey = otp_result.scalar_one_or_none()

        otp_value = None
        if one_time_prekey:
            otp_value = one_time_prekey.prekey
            one_time_prekey.used = True
            await self.db.flush()

        return {
            "identity_key": public_key.identity_key,
            "signed_prekey": public_key.signed_prekey,
            "signed_prekey_signature": public_key.signed_prekey_signature,
            "one_time_prekey": otp_value,
        }

    async def upload_prekeys(
        self,
        user_id: uuid.UUID,
        device_id: str,
        prekeys: list[str],
    ) -> int:
        """Загрузить дополнительные one-time prekeys."""
        public_key = await self.get_user_public_key(user_id, device_id)
        if not public_key:
            raise ValueError("Ключи устройства не найдены")

        max_id_result = await self.db.execute(
            select(OneTimePrekey.key_id)
            .where(OneTimePrekey.user_public_key_id == public_key.id)
            .order_by(OneTimePrekey.key_id.desc())
            .limit(1)
        )
        max_id = max_id_result.scalar() or 0

        for idx, prekey in enumerate(prekeys):
            otp = OneTimePrekey(
                user_public_key_id=public_key.id,
                key_id=max_id + idx + 1,
                prekey=prekey,
            )
            self.db.add(otp)

        await self.db.flush()
        return len(prekeys)

    async def get_prekeys_count(
        self,
        user_id: uuid.UUID,
        device_id: str,
    ) -> int:
        """Получить количество доступных prekeys."""
        public_key = await self.get_user_public_key(user_id, device_id)
        if not public_key:
            return 0

        result = await self.db.execute(
            select(OneTimePrekey)
            .where(OneTimePrekey.user_public_key_id == public_key.id)
            .where(OneTimePrekey.used == False)  # noqa: E712
        )
        return len(result.scalars().all())
