"""Сервис аутентификации [SECURITY]."""

import hashlib
import secrets
import uuid
from datetime import datetime, timedelta

from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
from jose import JWTError, jwt
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.config import get_settings
from src.models.user import User, UserSession

ph = PasswordHasher()


class AuthError(Exception):
    """Ошибка аутентификации."""

    def __init__(self, message: str, code: str = "auth_error"):
        self.message = message
        self.code = code
        super().__init__(message)


class AuthService:
    """Сервис аутентификации."""

    def __init__(self, db: AsyncSession):
        self.db = db
        self.settings = get_settings()

    def _hash_password(self, password: str) -> str:
        """Хеширование пароля с Argon2."""
        return ph.hash(password)

    def _verify_password(self, password: str, password_hash: str) -> bool:
        """Проверка пароля."""
        try:
            ph.verify(password_hash, password)
            return True
        except VerifyMismatchError:
            return False

    def _hash_token(self, token: str) -> str:
        """Хеширование refresh token для хранения."""
        return hashlib.sha256(token.encode()).hexdigest()

    def _create_access_token(self, user_id: uuid.UUID) -> str:
        """Создание access token."""
        expire = datetime.utcnow() + timedelta(
            minutes=self.settings.access_token_expire_minutes
        )
        payload = {
            "sub": str(user_id),
            "exp": expire,
            "type": "access",
        }
        token: str = jwt.encode(payload, self.settings.secret_key, algorithm="HS256")
        return token

    def _create_refresh_token(self) -> str:
        """Создание refresh token."""
        return secrets.token_urlsafe(32)

    def verify_access_token(self, token: str) -> uuid.UUID | None:
        """Проверка access token и возврат user_id."""
        try:
            payload = jwt.decode(
                token,
                self.settings.secret_key,
                algorithms=["HS256"],
            )
            if payload.get("type") != "access":
                return None
            user_id = payload.get("sub")
            if user_id is None:
                return None
            return uuid.UUID(user_id)
        except (JWTError, ValueError):
            return None

    async def register(
        self,
        email: str,
        password: str,
        name: str,
    ) -> User:
        """Регистрация нового пользователя."""
        existing = await self.db.execute(select(User).where(User.email == email))
        if existing.scalar_one_or_none():
            raise AuthError("Пользователь с таким email уже существует", "email_exists")

        user = User(
            email=email,
            password_hash=self._hash_password(password),
            name=name,
        )
        self.db.add(user)
        await self.db.flush()
        await self.db.refresh(user)
        return user

    async def login(
        self,
        email: str,
        password: str,
        device_info: str | None = None,
        ip_address: str | None = None,
    ) -> tuple[User, str, str]:
        """Вход пользователя. Возвращает (user, access_token, refresh_token)."""
        result = await self.db.execute(select(User).where(User.email == email))
        user = result.scalar_one_or_none()

        if not user or not self._verify_password(password, user.password_hash):
            raise AuthError("Неверный email или пароль", "invalid_credentials")

        if not user.is_active:
            raise AuthError("Аккаунт деактивирован", "account_inactive")

        access_token = self._create_access_token(user.id)
        refresh_token = self._create_refresh_token()

        session = UserSession(
            user_id=user.id,
            refresh_token_hash=self._hash_token(refresh_token),
            device_info=device_info,
            ip_address=ip_address,
            expires_at=datetime.utcnow()
            + timedelta(days=self.settings.refresh_token_expire_days),
        )
        self.db.add(session)
        await self.db.flush()

        return user, access_token, refresh_token

    async def refresh_tokens(
        self,
        refresh_token: str,
        device_info: str | None = None,
        ip_address: str | None = None,
    ) -> tuple[str, str]:
        """Обновление токенов. Возвращает (access_token, new_refresh_token)."""
        token_hash = self._hash_token(refresh_token)

        result = await self.db.execute(
            select(UserSession)
            .where(UserSession.refresh_token_hash == token_hash)
            .where(UserSession.expires_at > datetime.utcnow())
        )
        session = result.scalar_one_or_none()

        if not session:
            raise AuthError("Невалидный или истёкший refresh token", "invalid_token")

        new_refresh_token = self._create_refresh_token()
        session.refresh_token_hash = self._hash_token(new_refresh_token)
        session.last_used_at = datetime.utcnow()
        session.expires_at = datetime.utcnow() + timedelta(
            days=self.settings.refresh_token_expire_days
        )
        if device_info:
            session.device_info = device_info
        if ip_address:
            session.ip_address = ip_address

        await self.db.flush()

        access_token = self._create_access_token(session.user_id)
        return access_token, new_refresh_token

    async def logout(self, refresh_token: str) -> None:
        """Выход — удаление сессии."""
        token_hash = self._hash_token(refresh_token)
        result = await self.db.execute(
            select(UserSession).where(UserSession.refresh_token_hash == token_hash)
        )
        session = result.scalar_one_or_none()
        if session:
            await self.db.delete(session)

    async def logout_all(self, user_id: uuid.UUID) -> int:
        """Выход со всех устройств. Возвращает количество удалённых сессий."""
        result = await self.db.execute(
            select(UserSession).where(UserSession.user_id == user_id)
        )
        sessions = result.scalars().all()
        count = len(sessions)
        for session in sessions:
            await self.db.delete(session)
        return count

    async def get_user_by_id(self, user_id: uuid.UUID) -> User | None:
        """Получить пользователя по ID."""
        result = await self.db.execute(select(User).where(User.id == user_id))
        return result.scalar_one_or_none()

    async def get_user_sessions(self, user_id: uuid.UUID) -> list[UserSession]:
        """Получить все активные сессии пользователя."""
        result = await self.db.execute(
            select(UserSession)
            .where(UserSession.user_id == user_id)
            .where(UserSession.expires_at > datetime.utcnow())
            .order_by(UserSession.last_used_at.desc())
        )
        return list(result.scalars().all())
