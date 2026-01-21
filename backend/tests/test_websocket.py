"""Тесты WebSocket менеджера."""

import uuid

from src.websocket.manager import ConnectionManager, UserConnection


class TestUserConnection:
    """Тесты UserConnection."""

    def test_user_connection_creation(self):
        """Создание UserConnection."""
        user_id = uuid.uuid4()
        conn = UserConnection(sid="test_sid", user_id=user_id)

        assert conn.sid == "test_sid"
        assert conn.user_id == user_id


class TestConnectionManager:
    """Тесты ConnectionManager."""

    def test_manager_initialization(self):
        """Инициализация менеджера."""
        mgr = ConnectionManager()

        assert mgr.sio is not None
        assert mgr.app is not None
        assert mgr._connections == {}
        assert mgr._user_sids == {}

    def test_is_user_online_false_when_not_connected(self):
        """Пользователь не онлайн, если не подключен."""
        mgr = ConnectionManager()
        user_id = uuid.uuid4()

        assert mgr.is_user_online(user_id) is False

    def test_is_user_online_true_when_connected(self):
        """Пользователь онлайн, если есть соединение."""
        mgr = ConnectionManager()
        user_id = uuid.uuid4()
        sid = "test_sid"

        mgr._connections[sid] = UserConnection(sid=sid, user_id=user_id)
        mgr._user_sids[user_id] = {sid}

        assert mgr.is_user_online(user_id) is True

    def test_multiple_connections_for_user(self):
        """Несколько соединений для одного пользователя."""
        mgr = ConnectionManager()
        user_id = uuid.uuid4()

        mgr._user_sids[user_id] = {"sid1", "sid2", "sid3"}
        mgr._connections["sid1"] = UserConnection(sid="sid1", user_id=user_id)
        mgr._connections["sid2"] = UserConnection(sid="sid2", user_id=user_id)
        mgr._connections["sid3"] = UserConnection(sid="sid3", user_id=user_id)

        assert mgr.is_user_online(user_id) is True
        assert len(mgr._user_sids[user_id]) == 3
