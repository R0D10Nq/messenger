"""Тесты 2FA [SECURITY]."""

import pyotp

from src.services.totp import TOTPService


class TestTOTPService:
    """Тесты сервиса TOTP."""

    def test_generate_secret(self):
        """Генерация секрета."""
        secret = TOTPService.generate_secret()
        assert len(secret) == 32
        assert secret.isalnum()

    def test_verify_code_valid(self):
        """Проверка валидного кода."""
        secret = TOTPService.generate_secret()
        totp = pyotp.TOTP(secret)
        code = totp.now()
        assert TOTPService.verify_code(secret, code) is True

    def test_verify_code_invalid(self):
        """Проверка невалидного кода."""
        secret = TOTPService.generate_secret()
        assert TOTPService.verify_code(secret, "000000") is False

    def test_generate_provisioning_uri(self):
        """Генерация provisioning URI."""
        secret = "JBSWY3DPEHPK3PXP"
        email = "test@example.com"
        uri = TOTPService.generate_provisioning_uri(secret, email)
        assert "otpauth://totp/" in uri
        assert "test" in uri and "example.com" in uri
        assert "MyMessenger" in uri

    def test_generate_qr_code_base64(self):
        """Генерация QR-кода в base64."""
        uri = "otpauth://totp/MyMessenger:test@example.com?secret=JBSWY3DPEHPK3PXP&issuer=MyMessenger"
        qr_code = TOTPService.generate_qr_code_base64(uri)
        assert isinstance(qr_code, str)
        assert len(qr_code) > 100


class TestTOTPSchemas:
    """Тесты схем 2FA."""

    def test_verify_2fa_request_valid(self):
        """Verify2FARequest валидация."""
        from src.schemas.totp import Verify2FARequest

        data = Verify2FARequest(code="123456")
        assert data.code == "123456"

    def test_verify_2fa_response(self):
        """Verify2FAResponse валидация."""
        from src.schemas.totp import Verify2FAResponse

        data = Verify2FAResponse(success=True, message="OK")
        assert data.success is True
        assert data.message == "OK"

    def test_setup_2fa_response(self):
        """Setup2FAResponse валидация."""
        from src.schemas.totp import Setup2FAResponse

        data = Setup2FAResponse(
            secret="JBSWY3DPEHPK3PXP",
            provisioning_uri="otpauth://totp/...",
            qr_code="base64data...",
        )
        assert data.secret == "JBSWY3DPEHPK3PXP"

    def test_two_factor_status_response(self):
        """TwoFactorStatusResponse валидация."""
        from src.schemas.totp import TwoFactorStatusResponse

        data = TwoFactorStatusResponse(enabled=True)
        assert data.enabled is True

    def test_login_with_2fa_request(self):
        """LoginWith2FARequest валидация."""
        from src.schemas.totp import LoginWith2FARequest

        data = LoginWith2FARequest(code="654321")
        assert data.code == "654321"
