"""API эндпоинты профиля и контактов."""

import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.deps import get_current_user
from src.db import get_db
from src.models.contact import Contact, ContactStatus
from src.models.user import User
from src.schemas.auth import UserResponse
from src.schemas.profile import (
    ContactCreateRequest,
    ContactListResponse,
    ContactResponse,
    ContactUpdateRequest,
    ProfileUpdateRequest,
)

router = APIRouter(prefix="/profile", tags=["profile"])


@router.get("/me", response_model=UserResponse)
async def get_my_profile(
    current_user: User = Depends(get_current_user),
) -> UserResponse:
    """Получить свой профиль."""
    return UserResponse.model_validate(current_user)


@router.patch("/me", response_model=UserResponse)
async def update_my_profile(
    data: ProfileUpdateRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> UserResponse:
    """Обновить свой профиль."""
    if data.name is not None:
        current_user.name = data.name
    if data.avatar_url is not None:
        current_user.avatar_url = data.avatar_url
    if data.status_message is not None:
        current_user.status_message = data.status_message

    await db.flush()
    await db.refresh(current_user)
    return UserResponse.model_validate(current_user)


@router.get("/contacts", response_model=ContactListResponse)
async def get_contacts(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> ContactListResponse:
    """Получить список контактов."""
    result = await db.execute(
        select(Contact)
        .where(Contact.owner_id == current_user.id)
        .where(Contact.status != ContactStatus.BLOCKED.value)
        .order_by(Contact.created_at.desc())
    )
    contacts = result.scalars().all()

    contact_responses = []
    for contact in contacts:
        contact_user = await db.get(User, contact.contact_id)
        if contact_user:
            contact_responses.append(
                ContactResponse(
                    id=contact.id,
                    contact_id=contact.contact_id,
                    nickname=contact.nickname,
                    status=contact.status,
                    contact_name=contact_user.name,
                    contact_email=contact_user.email,
                    contact_avatar_url=contact_user.avatar_url,
                    contact_status_message=contact_user.status_message,
                    created_at=contact.created_at,
                )
            )

    return ContactListResponse(contacts=contact_responses, total=len(contact_responses))


@router.post("/contacts", response_model=ContactResponse, status_code=status.HTTP_201_CREATED)
async def add_contact(
    data: ContactCreateRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> ContactResponse:
    """Добавить контакт."""
    if data.contact_id == current_user.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"message": "Нельзя добавить себя в контакты", "code": "self_contact"},
        )

    contact_user = await db.get(User, data.contact_id)
    if not contact_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"message": "Пользователь не найден", "code": "user_not_found"},
        )

    existing = await db.execute(
        select(Contact)
        .where(Contact.owner_id == current_user.id)
        .where(Contact.contact_id == data.contact_id)
    )
    if existing.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"message": "Контакт уже существует", "code": "contact_exists"},
        )

    contact = Contact(
        owner_id=current_user.id,
        contact_id=data.contact_id,
        nickname=data.nickname,
        status=ContactStatus.ACCEPTED.value,
    )
    db.add(contact)
    await db.flush()
    await db.refresh(contact)

    return ContactResponse(
        id=contact.id,
        contact_id=contact.contact_id,
        nickname=contact.nickname,
        status=contact.status,
        contact_name=contact_user.name,
        contact_email=contact_user.email,
        contact_avatar_url=contact_user.avatar_url,
        contact_status_message=contact_user.status_message,
        created_at=contact.created_at,
    )


@router.patch("/contacts/{contact_id}", response_model=ContactResponse)
async def update_contact(
    contact_id: uuid.UUID,
    data: ContactUpdateRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> ContactResponse:
    """Обновить контакт (nickname)."""
    result = await db.execute(
        select(Contact)
        .where(Contact.id == contact_id)
        .where(Contact.owner_id == current_user.id)
    )
    contact = result.scalar_one_or_none()

    if not contact:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"message": "Контакт не найден", "code": "contact_not_found"},
        )

    if data.nickname is not None:
        contact.nickname = data.nickname

    await db.flush()
    await db.refresh(contact)

    contact_user = await db.get(User, contact.contact_id)
    if not contact_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"message": "Пользователь не найден", "code": "user_not_found"},
        )

    return ContactResponse(
        id=contact.id,
        contact_id=contact.contact_id,
        nickname=contact.nickname,
        status=contact.status,
        contact_name=contact_user.name,
        contact_email=contact_user.email,
        contact_avatar_url=contact_user.avatar_url,
        contact_status_message=contact_user.status_message,
        created_at=contact.created_at,
    )


@router.delete("/contacts/{contact_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_contact(
    contact_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> None:
    """Удалить контакт."""
    result = await db.execute(
        select(Contact)
        .where(Contact.id == contact_id)
        .where(Contact.owner_id == current_user.id)
    )
    contact = result.scalar_one_or_none()

    if not contact:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"message": "Контакт не найден", "code": "contact_not_found"},
        )

    await db.delete(contact)


@router.post("/contacts/{contact_id}/block", status_code=status.HTTP_204_NO_CONTENT)
async def block_contact(
    contact_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> None:
    """Заблокировать контакт."""
    result = await db.execute(
        select(Contact)
        .where(Contact.id == contact_id)
        .where(Contact.owner_id == current_user.id)
    )
    contact = result.scalar_one_or_none()

    if not contact:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"message": "Контакт не найден", "code": "contact_not_found"},
        )

    contact.status = ContactStatus.BLOCKED.value
    await db.flush()
