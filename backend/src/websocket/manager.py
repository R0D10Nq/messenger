"""Менеджер WebSocket соединений."""

from __future__ import annotations

import uuid
from dataclasses import dataclass
from typing import Any

import socketio

from src.config import get_settings
from src.services.auth import AuthService


@dataclass
class UserConnection:
    """Информация о соединении пользователя."""

    sid: str
    user_id: uuid.UUID


class ConnectionManager:
    """Менеджер WebSocket соединений."""

    def __init__(self) -> None:
        settings = get_settings()
        self.sio = socketio.AsyncServer(
            async_mode="asgi",
            cors_allowed_origins=settings.cors_origins,
            logger=settings.debug,
            engineio_logger=settings.debug,
        )
        self.app = socketio.ASGIApp(self.sio)

        self._connections: dict[str, UserConnection] = {}
        self._user_sids: dict[uuid.UUID, set[str]] = {}

        self._register_handlers()

    def _register_handlers(self) -> None:  # noqa: C901
        """Регистрация обработчиков событий."""

        @self.sio.event  # type: ignore[untyped-decorator]
        async def connect(
            sid: str, environ: dict[str, Any], auth: dict[str, Any] | None
        ) -> bool:
            """Обработка подключения."""
            if not auth or "token" not in auth:
                return False

            token = auth["token"]
            auth_service = AuthService(db=None)  # type: ignore[arg-type]
            user_id = auth_service.verify_access_token(token)

            if not user_id:
                return False

            self._connections[sid] = UserConnection(sid=sid, user_id=user_id)

            if user_id not in self._user_sids:
                self._user_sids[user_id] = set()
            self._user_sids[user_id].add(sid)

            return True

        @self.sio.event  # type: ignore[untyped-decorator]
        async def disconnect(sid: str) -> None:
            """Обработка отключения."""
            conn = self._connections.pop(sid, None)
            if conn and conn.user_id in self._user_sids:
                self._user_sids[conn.user_id].discard(sid)
                if not self._user_sids[conn.user_id]:
                    del self._user_sids[conn.user_id]

        @self.sio.event  # type: ignore[untyped-decorator]
        async def join_chat(sid: str, data: dict[str, Any]) -> dict[str, Any]:
            """Присоединиться к комнате чата."""
            conn = self._connections.get(sid)
            if not conn:
                return {"error": "Не авторизован"}

            chat_id = data.get("chat_id")
            if not chat_id:
                return {"error": "chat_id обязателен"}

            room = f"chat:{chat_id}"
            await self.sio.enter_room(sid, room)
            return {"status": "ok", "room": room}

        @self.sio.event  # type: ignore[untyped-decorator]
        async def leave_chat(sid: str, data: dict[str, Any]) -> dict[str, Any]:
            """Покинуть комнату чата."""
            chat_id = data.get("chat_id")
            if not chat_id:
                return {"error": "chat_id обязателен"}

            room = f"chat:{chat_id}"
            await self.sio.leave_room(sid, room)
            return {"status": "ok"}

        @self.sio.event  # type: ignore[untyped-decorator]
        async def typing(sid: str, data: dict[str, Any]) -> None:
            """Индикация набора текста."""
            conn = self._connections.get(sid)
            if not conn:
                return

            chat_id = data.get("chat_id")
            if not chat_id:
                return

            room = f"chat:{chat_id}"
            await self.sio.emit(
                "user_typing",
                {"chat_id": chat_id, "user_id": str(conn.user_id)},
                room=room,
                skip_sid=sid,
            )

    async def emit_new_message(
        self,
        chat_id: uuid.UUID,
        message_data: dict[str, Any],
    ) -> None:
        """Отправить новое сообщение в комнату чата."""
        room = f"chat:{chat_id}"
        await self.sio.emit("new_message", message_data, room=room)

    async def emit_message_edited(
        self,
        chat_id: uuid.UUID,
        message_data: dict[str, Any],
    ) -> None:
        """Отправить уведомление о редактировании сообщения."""
        room = f"chat:{chat_id}"
        await self.sio.emit("message_edited", message_data, room=room)

    async def emit_message_deleted(
        self,
        chat_id: uuid.UUID,
        message_id: uuid.UUID,
    ) -> None:
        """Отправить уведомление об удалении сообщения."""
        room = f"chat:{chat_id}"
        await self.sio.emit(
            "message_deleted",
            {"chat_id": str(chat_id), "message_id": str(message_id)},
            room=room,
        )

    async def emit_to_user(
        self,
        user_id: uuid.UUID,
        event: str,
        data: dict[str, Any],
    ) -> None:
        """Отправить событие конкретному пользователю."""
        sids = self._user_sids.get(user_id, set())
        for sid in sids:
            await self.sio.emit(event, data, to=sid)

    def is_user_online(self, user_id: uuid.UUID) -> bool:
        """Проверить, онлайн ли пользователь."""
        return user_id in self._user_sids and len(self._user_sids[user_id]) > 0


manager = ConnectionManager()
