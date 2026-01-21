"""Тесты E2E шифрования [SECURITY]."""

import uuid
from datetime import UTC, datetime


class TestEncryptionSchemas:
    """Тесты схем шифрования."""

    def test_register_keys_request(self):
        """RegisterKeysRequest валидация."""
        from src.schemas.encryption import RegisterKeysRequest

        data = RegisterKeysRequest(
            device_id="device-123",
            identity_key="base64_identity_key",
            signed_prekey="base64_signed_prekey",
            signed_prekey_signature="base64_signature",
            one_time_prekeys=["prekey1", "prekey2", "prekey3"],
        )
        assert data.device_id == "device-123"
        assert len(data.one_time_prekeys) == 3

    def test_register_keys_request_empty_prekeys(self):
        """RegisterKeysRequest с пустыми prekeys."""
        from src.schemas.encryption import RegisterKeysRequest

        data = RegisterKeysRequest(
            device_id="device-123",
            identity_key="base64_identity_key",
            signed_prekey="base64_signed_prekey",
            signed_prekey_signature="base64_signature",
        )
        assert data.one_time_prekeys == []

    def test_public_key_response(self):
        """PublicKeyResponse валидация."""
        from src.schemas.encryption import PublicKeyResponse

        now = datetime.now(UTC)
        data = PublicKeyResponse(
            id=uuid.uuid4(),
            user_id=uuid.uuid4(),
            device_id="device-123",
            identity_key="base64_identity_key",
            signed_prekey="base64_signed_prekey",
            signed_prekey_signature="base64_signature",
            created_at=now,
        )
        assert data.device_id == "device-123"

    def test_key_bundle_response(self):
        """KeyBundleResponse валидация."""
        from src.schemas.encryption import KeyBundleResponse

        data = KeyBundleResponse(
            identity_key="base64_identity_key",
            signed_prekey="base64_signed_prekey",
            signed_prekey_signature="base64_signature",
            one_time_prekey="base64_otp",
        )
        assert data.one_time_prekey == "base64_otp"

    def test_key_bundle_response_no_otp(self):
        """KeyBundleResponse без one-time prekey."""
        from src.schemas.encryption import KeyBundleResponse

        data = KeyBundleResponse(
            identity_key="base64_identity_key",
            signed_prekey="base64_signed_prekey",
            signed_prekey_signature="base64_signature",
            one_time_prekey=None,
        )
        assert data.one_time_prekey is None

    def test_upload_prekeys_request(self):
        """UploadPrekeysRequest валидация."""
        from src.schemas.encryption import UploadPrekeysRequest

        data = UploadPrekeysRequest(prekeys=["pk1", "pk2", "pk3"])
        assert len(data.prekeys) == 3

    def test_prekeys_count_response(self):
        """PrekeysCountResponse валидация."""
        from src.schemas.encryption import PrekeysCountResponse

        data = PrekeysCountResponse(count=50, device_id="device-123")
        assert data.count == 50
        assert data.device_id == "device-123"
