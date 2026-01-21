"""Pydantic схемы."""

from src.schemas.auth import (
    LoginRequest,
    RegisterRequest,
    TokenResponse,
    UserResponse,
)
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
from src.schemas.media import (
    AttachmentResponse,
    MediaFileResponse,
    UploadResponse,
)
from src.schemas.profile import (
    ContactCreateRequest,
    ContactListResponse,
    ContactResponse,
    ContactUpdateRequest,
    ProfileUpdateRequest,
)

__all__ = [
    "AddMembersRequest",
    "AttachmentResponse",
    "ChatListResponse",
    "ChatMemberResponse",
    "ChatResponse",
    "ContactCreateRequest",
    "ContactListResponse",
    "ContactResponse",
    "ContactUpdateRequest",
    "CreateDirectChatRequest",
    "CreateGroupChatRequest",
    "EditMessageRequest",
    "LoginRequest",
    "MediaFileResponse",
    "MessageListResponse",
    "MessageResponse",
    "ProfileUpdateRequest",
    "RegisterRequest",
    "SendMessageRequest",
    "TokenResponse",
    "UpdateGroupChatRequest",
    "UpdateMemberRoleRequest",
    "UploadResponse",
    "UserResponse",
]
