"""Pydantic схемы."""

from src.schemas.auth import (
    LoginRequest,
    RegisterRequest,
    TokenResponse,
    UserResponse,
)
from src.schemas.profile import (
    ContactCreateRequest,
    ContactListResponse,
    ContactResponse,
    ContactUpdateRequest,
    ProfileUpdateRequest,
)

__all__ = [
    "ContactCreateRequest",
    "ContactListResponse",
    "ContactResponse",
    "ContactUpdateRequest",
    "LoginRequest",
    "ProfileUpdateRequest",
    "RegisterRequest",
    "TokenResponse",
    "UserResponse",
]
