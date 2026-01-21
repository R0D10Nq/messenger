"""Тесты чатов и сообщений."""

import uuid
from datetime import UTC, datetime

from src.models.chat import ChatType, MessageStatus


class TestChatModels:
    """Тесты моделей чатов."""

    def test_chat_type_values(self):
        """Проверка значений типов чата."""
        assert ChatType.DIRECT.value == "direct"
        assert ChatType.GROUP.value == "group"

    def test_message_status_values(self):
        """Проверка значений статусов сообщений."""
        assert MessageStatus.SENT.value == "sent"
        assert MessageStatus.DELIVERED.value == "delivered"
        assert MessageStatus.READ.value == "read"


class TestChatSchemas:
    """Тесты схем чатов."""

    def test_create_direct_chat_request(self):
        """CreateDirectChatRequest валидация."""
        from src.schemas.chat import CreateDirectChatRequest

        user_id = uuid.uuid4()
        data = CreateDirectChatRequest(user_id=user_id)
        assert data.user_id == user_id

    def test_send_message_request(self):
        """SendMessageRequest валидация."""
        from src.schemas.chat import SendMessageRequest

        data = SendMessageRequest(content="Привет!")
        assert data.content == "Привет!"
        assert data.reply_to_id is None

    def test_send_message_request_with_reply(self):
        """SendMessageRequest с ответом."""
        from src.schemas.chat import SendMessageRequest

        reply_id = uuid.uuid4()
        data = SendMessageRequest(content="Ответ", reply_to_id=reply_id)
        assert data.content == "Ответ"
        assert data.reply_to_id == reply_id

    def test_edit_message_request(self):
        """EditMessageRequest валидация."""
        from src.schemas.chat import EditMessageRequest

        data = EditMessageRequest(content="Отредактировано")
        assert data.content == "Отредактировано"

    def test_message_response(self):
        """MessageResponse валидация."""
        from src.schemas.chat import MessageResponse

        now = datetime.now(UTC)
        data = MessageResponse(
            id=uuid.uuid4(),
            chat_id=uuid.uuid4(),
            sender_id=uuid.uuid4(),
            sender_name="Иван",
            content="Привет!",
            status="sent",
            reply_to_id=None,
            edited_at=None,
            created_at=now,
        )
        assert data.sender_name == "Иван"
        assert data.content == "Привет!"
        assert data.status == "sent"

    def test_chat_member_response(self):
        """ChatMemberResponse валидация."""
        from src.schemas.chat import ChatMemberResponse

        now = datetime.now(UTC)
        data = ChatMemberResponse(
            user_id=uuid.uuid4(),
            name="Иван",
            avatar_url=None,
            joined_at=now,
        )
        assert data.name == "Иван"

    def test_chat_response(self):
        """ChatResponse валидация."""
        from src.schemas.chat import ChatResponse

        now = datetime.now(UTC)
        data = ChatResponse(
            id=uuid.uuid4(),
            chat_type="direct",
            name=None,
            members=[],
            last_message=None,
            unread_count=0,
            created_at=now,
        )
        assert data.chat_type == "direct"
        assert data.unread_count == 0

    def test_chat_list_response(self):
        """ChatListResponse валидация."""
        from src.schemas.chat import ChatListResponse

        data = ChatListResponse(chats=[], total=0)
        assert data.chats == []
        assert data.total == 0

    def test_message_list_response(self):
        """MessageListResponse валидация."""
        from src.schemas.chat import MessageListResponse

        data = MessageListResponse(messages=[], total=0, has_more=False)
        assert data.messages == []
        assert data.has_more is False
