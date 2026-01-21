"""Тесты аутентификации [SECURITY]."""

import uuid
from datetime import UTC, datetime
from unittest.mock import AsyncMock, MagicMock

import pytest

from src.services.auth import AuthError, AuthService


class TestAuthService:
    """Тесты AuthService."""

    @pytest.fixture
    def mock_db(self):
        """Мок сессии БД."""
        db = AsyncMock()
        db.add = MagicMock()
        db.flush = AsyncMock()
        db.refresh = AsyncMock()
        db.delete = AsyncMock()
        return db

    @pytest.fixture
    def auth_service(self, mock_db):
        """Экземпляр AuthService с мок БД."""
        return AuthService(mock_db)

    def test_hash_password_returns_hash(self, auth_service):
        """Хеширование пароля должно возвращать хеш."""
        password = "test_password_123"
        hashed = auth_service._hash_password(password)

        assert hashed != password
        assert len(hashed) > 0

    def test_verify_password_correct(self, auth_service):
        """Проверка правильного пароля."""
        password = "test_password_123"
        hashed = auth_service._hash_password(password)

        assert auth_service._verify_password(password, hashed) is True

    def test_verify_password_incorrect(self, auth_service):
        """Проверка неправильного пароля."""
        password = "test_password_123"
        hashed = auth_service._hash_password(password)

        assert auth_service._verify_password("wrong_password", hashed) is False

    def test_create_access_token(self, auth_service):
        """Создание access token."""
        user_id = uuid.uuid4()
        token = auth_service._create_access_token(user_id)

        assert isinstance(token, str)
        assert len(token) > 0

    def test_verify_access_token_valid(self, auth_service):
        """Проверка валидного access token."""
        user_id = uuid.uuid4()
        token = auth_service._create_access_token(user_id)

        result = auth_service.verify_access_token(token)
        assert result == user_id

    def test_verify_access_token_invalid(self, auth_service):
        """Проверка невалидного access token."""
        result = auth_service.verify_access_token("invalid_token")
        assert result is None

    def test_create_refresh_token(self, auth_service):
        """Создание refresh token."""
        token = auth_service._create_refresh_token()

        assert isinstance(token, str)
        assert len(token) >= 32

    def test_hash_token(self, auth_service):
        """Хеширование токена."""
        token = "test_token"
        hashed = auth_service._hash_token(token)

        assert hashed != token
        assert len(hashed) == 64  # SHA256 hex

    @pytest.mark.asyncio
    async def test_register_creates_user(self, auth_service, mock_db):
        """Регистрация создаёт пользователя."""
        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = None
        mock_db.execute.return_value = mock_result

        async def refresh_side_effect(user):
            user.id = uuid.uuid4()
            user.created_at = datetime.now(UTC)

        mock_db.refresh.side_effect = refresh_side_effect

        user = await auth_service.register(
            email="test@example.com",
            password="password123",
            name="Test User",
        )

        assert user.email == "test@example.com"
        assert user.name == "Test User"
        mock_db.add.assert_called_once()
        mock_db.flush.assert_called_once()

    @pytest.mark.asyncio
    async def test_register_duplicate_email_raises(self, auth_service, mock_db):
        """Регистрация с существующим email вызывает ошибку."""
        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = MagicMock()  # existing user
        mock_db.execute.return_value = mock_result

        with pytest.raises(AuthError) as exc_info:
            await auth_service.register(
                email="existing@example.com",
                password="password123",
                name="Test User",
            )

        assert exc_info.value.code == "email_exists"


class TestAuthServicePasswordSecurity:
    """Тесты безопасности паролей."""

    @pytest.fixture
    def mock_db(self):
        """Мок сессии БД."""
        return AsyncMock()

    @pytest.fixture
    def auth_service(self, mock_db):
        """Экземпляр AuthService."""
        return AuthService(mock_db)

    def test_different_passwords_different_hashes(self, auth_service):
        """Разные пароли дают разные хеши."""
        hash1 = auth_service._hash_password("password1")
        hash2 = auth_service._hash_password("password2")

        assert hash1 != hash2

    def test_same_password_different_hashes(self, auth_service):
        """Один пароль при повторном хешировании даёт разные хеши (salt)."""
        password = "same_password"
        hash1 = auth_service._hash_password(password)
        hash2 = auth_service._hash_password(password)

        # Argon2 использует случайную соль
        assert hash1 != hash2
        # Но оба хеша валидны
        assert auth_service._verify_password(password, hash1)
        assert auth_service._verify_password(password, hash2)
