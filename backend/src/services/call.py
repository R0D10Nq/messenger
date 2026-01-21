"""Сервис для аудио/видео звонков."""

import uuid
from datetime import UTC, datetime

from sqlalchemy import or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.call import Call, CallStatus
from src.models.user import User


class CallService:
    """Сервис для управления звонками."""

    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def initiate_call(
        self,
        caller_id: uuid.UUID,
        callee_id: uuid.UUID,
        call_type: str,
    ) -> Call:
        """Инициировать звонок."""
        callee = await self.db.get(User, callee_id)
        if not callee:
            raise ValueError("Пользователь не найден")

        if caller_id == callee_id:
            raise ValueError("Нельзя позвонить самому себе")

        active_call = await self._get_active_call(caller_id)
        if active_call:
            raise ValueError("У вас уже есть активный звонок")

        call = Call(
            caller_id=caller_id,
            callee_id=callee_id,
            call_type=call_type,
            status=CallStatus.PENDING.value,
        )
        self.db.add(call)
        await self.db.flush()
        await self.db.refresh(call)

        return call

    async def accept_call(self, call_id: uuid.UUID, user_id: uuid.UUID) -> Call:
        """Принять звонок."""
        call = await self.db.get(Call, call_id)
        if not call:
            raise ValueError("Звонок не найден")

        if call.callee_id != user_id:
            raise ValueError("Вы не можете принять этот звонок")

        if call.status != CallStatus.PENDING.value:
            raise ValueError("Звонок уже не ожидает ответа")

        call.status = CallStatus.ACTIVE.value
        call.started_at = datetime.now(UTC)

        await self.db.flush()
        await self.db.refresh(call)

        return call

    async def decline_call(self, call_id: uuid.UUID, user_id: uuid.UUID) -> Call:
        """Отклонить звонок."""
        call = await self.db.get(Call, call_id)
        if not call:
            raise ValueError("Звонок не найден")

        if call.callee_id != user_id:
            raise ValueError("Вы не можете отклонить этот звонок")

        if call.status != CallStatus.PENDING.value:
            raise ValueError("Звонок уже не ожидает ответа")

        call.status = CallStatus.DECLINED.value
        call.ended_at = datetime.now(UTC)
        call.end_reason = "declined"

        await self.db.flush()
        await self.db.refresh(call)

        return call

    async def end_call(self, call_id: uuid.UUID, user_id: uuid.UUID) -> Call:
        """Завершить звонок."""
        call = await self.db.get(Call, call_id)
        if not call:
            raise ValueError("Звонок не найден")

        if call.caller_id != user_id and call.callee_id != user_id:
            raise ValueError("Вы не участник этого звонка")

        if call.status == CallStatus.ENDED.value:
            raise ValueError("Звонок уже завершён")

        call.status = CallStatus.ENDED.value
        call.ended_at = datetime.now(UTC)
        call.end_reason = "ended_by_user"

        if call.started_at:
            delta = call.ended_at - call.started_at
            call.duration_seconds = int(delta.total_seconds())

        await self.db.flush()
        await self.db.refresh(call)

        return call

    async def get_call(self, call_id: uuid.UUID) -> Call | None:
        """Получить звонок по ID."""
        return await self.db.get(Call, call_id)

    async def get_call_history(
        self,
        user_id: uuid.UUID,
        limit: int = 50,
        offset: int = 0,
    ) -> tuple[list[Call], int]:
        """Получить историю звонков."""
        query = select(Call).where(
            or_(Call.caller_id == user_id, Call.callee_id == user_id)
        )

        count_result = await self.db.execute(query)
        total = len(count_result.scalars().all())

        result = await self.db.execute(
            query.order_by(Call.created_at.desc()).offset(offset).limit(limit)
        )
        calls = list(result.scalars().all())

        return calls, total

    async def _get_active_call(self, user_id: uuid.UUID) -> Call | None:
        """Получить активный звонок пользователя."""
        result = await self.db.execute(
            select(Call)
            .where(
                or_(Call.caller_id == user_id, Call.callee_id == user_id),
                Call.status.in_([CallStatus.PENDING.value, CallStatus.ACTIVE.value]),
            )
            .limit(1)
        )
        return result.scalar_one_or_none()
