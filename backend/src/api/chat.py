"""API эндпоинты чатов и сообщений."""

import uuid
from datetime import UTC, datetime

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import and_, func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.api.deps import get_current_user
from src.db import get_db
from src.models.chat import Chat, ChatMember, ChatType, MemberRole, Message
from src.models.user import User
from src.schemas.chat import (
    AddMembersRequest,
    ChatListResponse,
    ChatMemberResponse,
    ChatResponse,
    CreateDirectChatRequest,
    CreateGroupChatRequest,
    EditMessageRequest,
    MessageListResponse,
    MessageResponse,
    SendMessageRequest,
    UpdateGroupChatRequest,
    UpdateMemberRoleRequest,
)

router = APIRouter(prefix="/chats", tags=["chats"])


async def _build_message_response(message: Message, db: AsyncSession) -> MessageResponse:
    """Построить ответ сообщения с данными отправителя."""
    sender = await db.get(User, message.sender_id)
    return MessageResponse(
        id=message.id,
        chat_id=message.chat_id,
        sender_id=message.sender_id,
        sender_name=sender.name if sender else "Удалённый пользователь",
        content=message.content,
        status=message.status,
        reply_to_id=message.reply_to_id,
        edited_at=message.edited_at,
        created_at=message.created_at,
    )


async def _build_chat_response(
    chat: Chat,
    current_user_id: uuid.UUID,
    db: AsyncSession,
) -> ChatResponse:
    """Построить ответ чата."""
    members_response = []
    for member in chat.members:
        user = await db.get(User, member.user_id)
        if user:
            members_response.append(
                ChatMemberResponse(
                    user_id=user.id,
                    name=user.name,
                    avatar_url=user.avatar_url,
                    role=member.role,
                    joined_at=member.joined_at,
                )
            )

    last_message_result = await db.execute(
        select(Message)
        .where(Message.chat_id == chat.id)
        .order_by(Message.created_at.desc())
        .limit(1)
    )
    last_message = last_message_result.scalar_one_or_none()
    last_message_response = None
    if last_message:
        last_message_response = await _build_message_response(last_message, db)

    member_record = next(
        (m for m in chat.members if m.user_id == current_user_id), None
    )
    unread_count = 0
    if member_record and member_record.last_read_at:
        unread_result = await db.execute(
            select(func.count(Message.id))
            .where(Message.chat_id == chat.id)
            .where(Message.created_at > member_record.last_read_at)
            .where(Message.sender_id != current_user_id)
        )
        unread_count = unread_result.scalar() or 0

    chat_name = chat.name
    if chat.chat_type == ChatType.DIRECT.value and not chat_name:
        other_member = next(
            (m for m in chat.members if m.user_id != current_user_id), None
        )
        if other_member:
            other_user = await db.get(User, other_member.user_id)
            chat_name = other_user.name if other_user else None

    return ChatResponse(
        id=chat.id,
        chat_type=chat.chat_type,
        name=chat_name,
        description=chat.description,
        avatar_url=chat.avatar_url,
        members=members_response,
        last_message=last_message_response,
        unread_count=unread_count,
        created_at=chat.created_at,
    )


@router.get("", response_model=ChatListResponse)
async def get_chats(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> ChatListResponse:
    """Получить список чатов пользователя."""
    result = await db.execute(
        select(Chat)
        .join(ChatMember)
        .where(ChatMember.user_id == current_user.id)
        .options(selectinload(Chat.members))
        .order_by(Chat.updated_at.desc())
    )
    chats = result.scalars().unique().all()

    chat_responses = []
    for chat in chats:
        chat_responses.append(await _build_chat_response(chat, current_user.id, db))

    return ChatListResponse(chats=chat_responses, total=len(chat_responses))


@router.post("/direct", response_model=ChatResponse, status_code=status.HTTP_201_CREATED)
async def create_direct_chat(
    data: CreateDirectChatRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> ChatResponse:
    """Создать прямой чат с пользователем."""
    if data.user_id == current_user.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"message": "Нельзя создать чат с самим собой", "code": "self_chat"},
        )

    other_user = await db.get(User, data.user_id)
    if not other_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"message": "Пользователь не найден", "code": "user_not_found"},
        )

    existing_chat = await db.execute(
        select(Chat)
        .join(ChatMember, Chat.id == ChatMember.chat_id)
        .where(Chat.chat_type == ChatType.DIRECT.value)
        .where(
            or_(
                and_(
                    ChatMember.user_id == current_user.id,
                    Chat.id.in_(
                        select(ChatMember.chat_id).where(ChatMember.user_id == data.user_id)
                    ),
                ),
                and_(
                    ChatMember.user_id == data.user_id,
                    Chat.id.in_(
                        select(ChatMember.chat_id).where(ChatMember.user_id == current_user.id)
                    ),
                ),
            )
        )
        .options(selectinload(Chat.members))
    )
    existing = existing_chat.scalars().first()
    if existing:
        return await _build_chat_response(existing, current_user.id, db)

    chat = Chat(chat_type=ChatType.DIRECT.value)
    db.add(chat)
    await db.flush()

    member1 = ChatMember(chat_id=chat.id, user_id=current_user.id)
    member2 = ChatMember(chat_id=chat.id, user_id=data.user_id)
    db.add(member1)
    db.add(member2)
    await db.flush()

    await db.refresh(chat)
    result = await db.execute(
        select(Chat).where(Chat.id == chat.id).options(selectinload(Chat.members))
    )
    chat = result.scalar_one()

    return await _build_chat_response(chat, current_user.id, db)


@router.get("/{chat_id}", response_model=ChatResponse)
async def get_chat(
    chat_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> ChatResponse:
    """Получить информацию о чате."""
    result = await db.execute(
        select(Chat)
        .where(Chat.id == chat_id)
        .options(selectinload(Chat.members))
    )
    chat = result.scalar_one_or_none()

    if not chat:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"message": "Чат не найден", "code": "chat_not_found"},
        )

    is_member = any(m.user_id == current_user.id for m in chat.members)
    if not is_member:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={"message": "Нет доступа к чату", "code": "access_denied"},
        )

    return await _build_chat_response(chat, current_user.id, db)


@router.get("/{chat_id}/messages", response_model=MessageListResponse)
async def get_messages(
    chat_id: uuid.UUID,
    limit: int = Query(50, ge=1, le=100),
    before: uuid.UUID | None = None,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> MessageListResponse:
    """Получить сообщения чата."""
    member_check = await db.execute(
        select(ChatMember)
        .where(ChatMember.chat_id == chat_id)
        .where(ChatMember.user_id == current_user.id)
    )
    if not member_check.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={"message": "Нет доступа к чату", "code": "access_denied"},
        )

    query = select(Message).where(Message.chat_id == chat_id)

    if before:
        before_msg = await db.get(Message, before)
        if before_msg:
            query = query.where(Message.created_at < before_msg.created_at)

    query = query.order_by(Message.created_at.desc()).limit(limit + 1)
    result = await db.execute(query)
    messages = list(result.scalars().all())

    has_more = len(messages) > limit
    if has_more:
        messages = messages[:limit]

    message_responses = []
    for msg in reversed(messages):
        message_responses.append(await _build_message_response(msg, db))

    return MessageListResponse(
        messages=message_responses,
        total=len(message_responses),
        has_more=has_more,
    )


@router.post(
    "/{chat_id}/messages",
    response_model=MessageResponse,
    status_code=status.HTTP_201_CREATED,
)
async def send_message(
    chat_id: uuid.UUID,
    data: SendMessageRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> MessageResponse:
    """Отправить сообщение в чат."""
    member_check = await db.execute(
        select(ChatMember)
        .where(ChatMember.chat_id == chat_id)
        .where(ChatMember.user_id == current_user.id)
    )
    if not member_check.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={"message": "Нет доступа к чату", "code": "access_denied"},
        )

    if data.reply_to_id:
        reply_msg = await db.get(Message, data.reply_to_id)
        if not reply_msg or reply_msg.chat_id != chat_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={"message": "Сообщение для ответа не найдено", "code": "reply_not_found"},
            )

    message = Message(
        chat_id=chat_id,
        sender_id=current_user.id,
        content=data.content,
        reply_to_id=data.reply_to_id,
    )
    db.add(message)

    chat_result = await db.execute(select(Chat).where(Chat.id == chat_id))
    chat = chat_result.scalar_one()
    chat.updated_at = datetime.now(UTC)

    await db.flush()
    await db.refresh(message)

    return await _build_message_response(message, db)


@router.patch("/{chat_id}/messages/{message_id}", response_model=MessageResponse)
async def edit_message(
    chat_id: uuid.UUID,
    message_id: uuid.UUID,
    data: EditMessageRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> MessageResponse:
    """Редактировать сообщение."""
    message = await db.get(Message, message_id)

    if not message or message.chat_id != chat_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"message": "Сообщение не найдено", "code": "message_not_found"},
        )

    if message.sender_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={"message": "Можно редактировать только свои сообщения", "code": "not_owner"},
        )

    message.content = data.content
    message.edited_at = datetime.now(UTC)
    await db.flush()
    await db.refresh(message)

    return await _build_message_response(message, db)


@router.delete("/{chat_id}/messages/{message_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_message(
    chat_id: uuid.UUID,
    message_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> None:
    """Удалить сообщение."""
    message = await db.get(Message, message_id)

    if not message or message.chat_id != chat_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"message": "Сообщение не найдено", "code": "message_not_found"},
        )

    if message.sender_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={"message": "Можно удалять только свои сообщения", "code": "not_owner"},
        )

    await db.delete(message)


@router.post("/{chat_id}/read", status_code=status.HTTP_204_NO_CONTENT)
async def mark_as_read(
    chat_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> None:
    """Отметить чат как прочитанный."""
    result = await db.execute(
        select(ChatMember)
        .where(ChatMember.chat_id == chat_id)
        .where(ChatMember.user_id == current_user.id)
    )
    member = result.scalar_one_or_none()

    if not member:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={"message": "Нет доступа к чату", "code": "access_denied"},
        )

    member.last_read_at = datetime.now(UTC)
    await db.flush()


@router.post("/group", response_model=ChatResponse, status_code=status.HTTP_201_CREATED)
async def create_group_chat(
    data: CreateGroupChatRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> ChatResponse:
    """Создать групповой чат."""
    chat = Chat(
        chat_type=ChatType.GROUP.value,
        name=data.name,
        description=data.description,
    )
    db.add(chat)
    await db.flush()

    owner_member = ChatMember(
        chat_id=chat.id,
        user_id=current_user.id,
        role=MemberRole.OWNER.value,
    )
    db.add(owner_member)

    for user_id in data.member_ids:
        if user_id == current_user.id:
            continue
        user = await db.get(User, user_id)
        if user:
            member = ChatMember(
                chat_id=chat.id,
                user_id=user_id,
                role=MemberRole.MEMBER.value,
            )
            db.add(member)

    await db.flush()

    result = await db.execute(
        select(Chat).where(Chat.id == chat.id).options(selectinload(Chat.members))
    )
    chat = result.scalar_one()

    return await _build_chat_response(chat, current_user.id, db)


@router.patch("/{chat_id}", response_model=ChatResponse)
async def update_group_chat(
    chat_id: uuid.UUID,
    data: UpdateGroupChatRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> ChatResponse:
    """Обновить групповой чат (только для owner/admin)."""
    result = await db.execute(
        select(Chat).where(Chat.id == chat_id).options(selectinload(Chat.members))
    )
    chat = result.scalar_one_or_none()

    if not chat:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"message": "Чат не найден", "code": "chat_not_found"},
        )

    if chat.chat_type != ChatType.GROUP.value:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"message": "Только групповые чаты можно редактировать", "code": "not_group"},
        )

    member = next((m for m in chat.members if m.user_id == current_user.id), None)
    if not member or member.role not in (MemberRole.OWNER.value, MemberRole.ADMIN.value):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={"message": "Нет прав на редактирование", "code": "forbidden"},
        )

    if data.name is not None:
        chat.name = data.name
    if data.description is not None:
        chat.description = data.description
    if data.avatar_url is not None:
        chat.avatar_url = data.avatar_url

    await db.flush()
    await db.refresh(chat)

    return await _build_chat_response(chat, current_user.id, db)


@router.post("/{chat_id}/members", status_code=status.HTTP_201_CREATED)
async def add_members(
    chat_id: uuid.UUID,
    data: AddMembersRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> dict[str, int]:
    """Добавить участников в групповой чат."""
    result = await db.execute(
        select(Chat).where(Chat.id == chat_id).options(selectinload(Chat.members))
    )
    chat = result.scalar_one_or_none()

    if not chat or chat.chat_type != ChatType.GROUP.value:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"message": "Групповой чат не найден", "code": "chat_not_found"},
        )

    member = next((m for m in chat.members if m.user_id == current_user.id), None)
    if not member or member.role not in (MemberRole.OWNER.value, MemberRole.ADMIN.value):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={"message": "Нет прав на добавление участников", "code": "forbidden"},
        )

    existing_ids = {m.user_id for m in chat.members}
    added = 0

    for user_id in data.user_ids:
        if user_id in existing_ids:
            continue
        user = await db.get(User, user_id)
        if user:
            new_member = ChatMember(
                chat_id=chat.id,
                user_id=user_id,
                role=MemberRole.MEMBER.value,
            )
            db.add(new_member)
            added += 1

    await db.flush()
    return {"added": added}


@router.delete("/{chat_id}/members/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_member(
    chat_id: uuid.UUID,
    user_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> None:
    """Удалить участника из группового чата."""
    result = await db.execute(
        select(Chat).where(Chat.id == chat_id).options(selectinload(Chat.members))
    )
    chat = result.scalar_one_or_none()

    if not chat or chat.chat_type != ChatType.GROUP.value:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"message": "Групповой чат не найден", "code": "chat_not_found"},
        )

    current_member = next((m for m in chat.members if m.user_id == current_user.id), None)
    target_member = next((m for m in chat.members if m.user_id == user_id), None)

    if not target_member:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"message": "Участник не найден", "code": "member_not_found"},
        )

    is_self_leave = user_id == current_user.id
    is_admin = current_member and current_member.role in (
        MemberRole.OWNER.value, MemberRole.ADMIN.value
    )

    if not is_self_leave and not is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={"message": "Нет прав на удаление участников", "code": "forbidden"},
        )

    if target_member.role == MemberRole.OWNER.value:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"message": "Нельзя удалить владельца группы", "code": "cannot_remove_owner"},
        )

    await db.delete(target_member)


@router.patch("/{chat_id}/members/{user_id}/role")
async def update_member_role(
    chat_id: uuid.UUID,
    user_id: uuid.UUID,
    data: UpdateMemberRoleRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> dict[str, str]:
    """Изменить роль участника."""
    result = await db.execute(
        select(Chat).where(Chat.id == chat_id).options(selectinload(Chat.members))
    )
    chat = result.scalar_one_or_none()

    if not chat or chat.chat_type != ChatType.GROUP.value:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"message": "Групповой чат не найден", "code": "chat_not_found"},
        )

    current_member = next((m for m in chat.members if m.user_id == current_user.id), None)
    if not current_member or current_member.role != MemberRole.OWNER.value:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={"message": "Только владелец может менять роли", "code": "owner_only"},
        )

    target_member = next((m for m in chat.members if m.user_id == user_id), None)
    if not target_member:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"message": "Участник не найден", "code": "member_not_found"},
        )

    if target_member.role == MemberRole.OWNER.value:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"message": "Нельзя изменить роль владельца", "code": "cannot_change_owner"},
        )

    target_member.role = data.role
    await db.flush()

    return {"role": data.role}
