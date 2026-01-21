"""Схемы для стикеров и GIF."""

import uuid
from datetime import datetime

from pydantic import BaseModel, Field


class StickerPackCreate(BaseModel):
    """Запрос на создание набора стикеров."""

    name: str = Field(..., min_length=1, max_length=100)
    description: str | None = Field(None, max_length=500)
    is_animated: bool = False


class StickerCreate(BaseModel):
    """Запрос на добавление стикера в набор."""

    pack_id: uuid.UUID
    emoji: str = Field(..., max_length=10)
    file_url: str = Field(..., max_length=500)


class StickerResponse(BaseModel):
    """Ответ со стикером."""

    id: uuid.UUID
    pack_id: uuid.UUID
    emoji: str
    file_url: str
    is_animated: bool

    model_config = {"from_attributes": True}


class StickerPackResponse(BaseModel):
    """Ответ с набором стикеров."""

    id: uuid.UUID
    name: str
    description: str | None
    cover_url: str | None
    is_animated: bool
    sticker_count: int
    author_id: uuid.UUID
    is_official: bool
    created_at: datetime

    model_config = {"from_attributes": True}


class StickerPackDetailResponse(BaseModel):
    """Детальный ответ с набором стикеров и списком стикеров."""

    id: uuid.UUID
    name: str
    description: str | None
    cover_url: str | None
    is_animated: bool
    is_official: bool
    author_id: uuid.UUID
    stickers: list[StickerResponse]
    created_at: datetime

    model_config = {"from_attributes": True}


class GifSearchRequest(BaseModel):
    """Запрос на поиск GIF."""

    query: str = Field(..., min_length=1, max_length=100)
    limit: int = Field(20, ge=1, le=50)
    offset: int = Field(0, ge=0)


class GifResponse(BaseModel):
    """Ответ с GIF."""

    id: str
    title: str
    url: str
    preview_url: str
    width: int
    height: int


class GifSearchResponse(BaseModel):
    """Ответ с результатами поиска GIF."""

    gifs: list[GifResponse]
    total: int
    next_offset: int | None


class TrendingGifsResponse(BaseModel):
    """Ответ с популярными GIF."""

    gifs: list[GifResponse]


class UserStickerPacksResponse(BaseModel):
    """Список наборов стикеров пользователя."""

    packs: list[StickerPackResponse]
    total: int


class RecentStickersResponse(BaseModel):
    """Недавно использованные стикеры."""

    stickers: list[StickerResponse]
