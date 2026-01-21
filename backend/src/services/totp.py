"""Сервис двухфакторной аутентификации (2FA) [SECURITY]."""

import base64
import io
import uuid
from datetime import UTC, datetime

import pyotp
import qrcode
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.user import User


class TOTPService:
    """Сервис для работы с TOTP (Time-based One-Time Password)."""

    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    @staticmethod
    def generate_secret() -> str:
        """Сгенерировать секретный ключ для TOTP."""
        return pyotp.random_base32()

    @staticmethod
    def get_totp(secret: str) -> pyotp.TOTP:
        """Получить TOTP объект."""
        return pyotp.TOTP(secret)

    @staticmethod
    def verify_code(secret: str, code: str) -> bool:
        """Проверить TOTP код."""
        totp = pyotp.TOTP(secret)
        return totp.verify(code, valid_window=1)

    @staticmethod
    def generate_provisioning_uri(secret: str, email: str, issuer: str = "MyMessenger") -> str:
        """Сгенерировать URI для добавления в аутентификатор."""
        totp = pyotp.TOTP(secret)
        return totp.provisioning_uri(name=email, issuer_name=issuer)

    @staticmethod
    def generate_qr_code_base64(provisioning_uri: str) -> str:
        """Сгенерировать QR-код в формате base64."""
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(provisioning_uri)
        qr.make(fit=True)

        img = qr.make_image(fill_color="black", back_color="white")
        buffer = io.BytesIO()
        img.save(buffer, format="PNG")
        buffer.seek(0)

        return base64.b64encode(buffer.getvalue()).decode("utf-8")

    async def setup_2fa(self, user_id: uuid.UUID) -> dict[str, str]:
        """Настроить 2FA для пользователя (шаг 1: генерация секрета)."""
        user = await self.db.get(User, user_id)
        if not user:
            raise ValueError("Пользователь не найден")

        if user.totp_enabled:
            raise ValueError("2FA уже включена")

        secret = self.generate_secret()
        user.totp_secret = secret

        await self.db.flush()

        provisioning_uri = self.generate_provisioning_uri(secret, user.email)
        qr_code = self.generate_qr_code_base64(provisioning_uri)

        return {
            "secret": secret,
            "provisioning_uri": provisioning_uri,
            "qr_code": qr_code,
        }

    async def verify_and_enable_2fa(self, user_id: uuid.UUID, code: str) -> bool:
        """Подтвердить и включить 2FA (шаг 2: верификация кода)."""
        user = await self.db.get(User, user_id)
        if not user:
            raise ValueError("Пользователь не найден")

        if user.totp_enabled:
            raise ValueError("2FA уже включена")

        if not user.totp_secret:
            raise ValueError("Сначала выполните setup_2fa")

        if not self.verify_code(user.totp_secret, code):
            return False

        user.totp_enabled = True
        user.totp_verified_at = datetime.now(UTC)

        await self.db.flush()

        return True

    async def disable_2fa(self, user_id: uuid.UUID, code: str) -> bool:
        """Отключить 2FA."""
        user = await self.db.get(User, user_id)
        if not user:
            raise ValueError("Пользователь не найден")

        if not user.totp_enabled:
            raise ValueError("2FA не включена")

        if not user.totp_secret:
            raise ValueError("2FA не настроена")

        if not self.verify_code(user.totp_secret, code):
            return False

        user.totp_enabled = False
        user.totp_secret = None
        user.totp_verified_at = None

        await self.db.flush()

        return True

    async def verify_2fa_code(self, user_id: uuid.UUID, code: str) -> bool:
        """Проверить 2FA код при логине."""
        user = await self.db.get(User, user_id)
        if not user:
            return False

        if not user.totp_enabled or not user.totp_secret:
            return False

        return self.verify_code(user.totp_secret, code)

    async def is_2fa_enabled(self, user_id: uuid.UUID) -> bool:
        """Проверить, включена ли 2FA."""
        user = await self.db.get(User, user_id)
        if not user:
            return False

        return user.totp_enabled
