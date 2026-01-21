"""Тесты профиля и контактов."""

import uuid

from src.models.contact import ContactStatus


class TestContactStatus:
    """Тесты статусов контактов."""

    def test_contact_status_values(self):
        """Проверка значений статусов."""
        assert ContactStatus.PENDING.value == "pending"
        assert ContactStatus.ACCEPTED.value == "accepted"
        assert ContactStatus.BLOCKED.value == "blocked"

    def test_contact_status_is_string_enum(self):
        """ContactStatus должен быть строковым enum."""
        assert isinstance(ContactStatus.PENDING, str)
        assert ContactStatus.PENDING == "pending"


class TestProfileSchemas:
    """Тесты схем профиля."""

    def test_profile_update_request_optional_fields(self):
        """Все поля ProfileUpdateRequest опциональны."""
        from src.schemas.profile import ProfileUpdateRequest

        data = ProfileUpdateRequest()
        assert data.name is None
        assert data.avatar_url is None
        assert data.status_message is None

    def test_profile_update_request_with_values(self):
        """ProfileUpdateRequest с заполненными полями."""
        from src.schemas.profile import ProfileUpdateRequest

        data = ProfileUpdateRequest(
            name="Новое имя",
            avatar_url="https://example.com/avatar.png",
            status_message="Привет!",
        )
        assert data.name == "Новое имя"
        assert data.avatar_url == "https://example.com/avatar.png"
        assert data.status_message == "Привет!"

    def test_contact_create_request(self):
        """ContactCreateRequest валидация."""
        from src.schemas.profile import ContactCreateRequest

        contact_id = uuid.uuid4()
        data = ContactCreateRequest(contact_id=contact_id, nickname="Друг")
        assert data.contact_id == contact_id
        assert data.nickname == "Друг"

    def test_contact_create_request_without_nickname(self):
        """ContactCreateRequest без nickname."""
        from src.schemas.profile import ContactCreateRequest

        contact_id = uuid.uuid4()
        data = ContactCreateRequest(contact_id=contact_id)
        assert data.contact_id == contact_id
        assert data.nickname is None

    def test_contact_response(self):
        """ContactResponse валидация."""
        from datetime import UTC, datetime

        from src.schemas.profile import ContactResponse

        now = datetime.now(UTC)
        data = ContactResponse(
            id=uuid.uuid4(),
            contact_id=uuid.uuid4(),
            nickname="Друг",
            status="accepted",
            contact_name="Иван",
            contact_email="ivan@example.com",
            contact_avatar_url=None,
            contact_status_message="Онлайн",
            created_at=now,
        )
        assert data.nickname == "Друг"
        assert data.contact_name == "Иван"
        assert data.status == "accepted"

    def test_contact_list_response(self):
        """ContactListResponse валидация."""
        from src.schemas.profile import ContactListResponse

        data = ContactListResponse(contacts=[], total=0)
        assert data.contacts == []
        assert data.total == 0
