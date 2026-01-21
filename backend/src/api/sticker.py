"""API эндпоинты для стикеров и GIF."""

import uuid
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.deps import get_current_user
from src.db import get_db
from src.models.user import User
from src.schemas.sticker import (
    GifResponse,
    GifSearchResponse,
    RecentStickersResponse,
    StickerPackCreate,
    StickerPackDetailResponse,
    StickerPackResponse,
    StickerResponse,
    TrendingGifsResponse,
    UserStickerPacksResponse,
)

router = APIRouter(prefix="/stickers", tags=["stickers"])


DEMO_STICKER_PACKS = [
    {
        "id": "550e8400-e29b-41d4-a716-446655440001",
        "name": "Котики",
        "description": "Милые котики для любого настроения",
        "cover_url": "/stickers/cats/cover.webp",
        "is_animated": False,
        "sticker_count": 12,
        "author_id": "550e8400-e29b-41d4-a716-446655440000",
        "is_official": True,
        "stickers": [
            {"id": f"cat-{i}", "emoji": "😺", "file_url": f"/stickers/cats/{i}.webp", "is_animated": False}
            for i in range(1, 13)
        ],
    },
    {
        "id": "550e8400-e29b-41d4-a716-446655440002",
        "name": "Эмоции",
        "description": "Выразительные эмодзи-стикеры",
        "cover_url": "/stickers/emotions/cover.webp",
        "is_animated": True,
        "sticker_count": 8,
        "author_id": "550e8400-e29b-41d4-a716-446655440000",
        "is_official": True,
        "stickers": [
            {"id": f"emotion-{i}", "emoji": "😀", "file_url": f"/stickers/emotions/{i}.webp", "is_animated": True}
            for i in range(1, 9)
        ],
    },
]

DEMO_GIFS = [
    {"id": "gif1", "title": "Танцующий кот", "url": "https://media.giphy.com/media/cat.gif", "preview_url": "https://media.giphy.com/media/cat_s.gif", "width": 200, "height": 200},
    {"id": "gif2", "title": "Аплодисменты", "url": "https://media.giphy.com/media/clap.gif", "preview_url": "https://media.giphy.com/media/clap_s.gif", "width": 200, "height": 150},
]


@router.get("/packs", response_model=UserStickerPacksResponse)
async def get_sticker_packs(
    current_user: User = Depends(get_current_user),
) -> UserStickerPacksResponse:
    """Получить список наборов стикеров пользователя."""
    packs = [
        StickerPackResponse(
            id=uuid.UUID(p["id"]),
            name=p["name"],
            description=p["description"],
            cover_url=p["cover_url"],
            is_animated=p["is_animated"],
            sticker_count=p["sticker_count"],
            author_id=uuid.UUID(p["author_id"]),
            is_official=p["is_official"],
            created_at=datetime.now(),
        )
        for p in DEMO_STICKER_PACKS
    ]
    return UserStickerPacksResponse(packs=packs, total=len(packs))


@router.get("/packs/{pack_id}", response_model=StickerPackDetailResponse)
async def get_sticker_pack(
    pack_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
) -> StickerPackDetailResponse:
    """Получить детали набора стикеров."""
    pack = next((p for p in DEMO_STICKER_PACKS if p["id"] == str(pack_id)), None)
    if not pack:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"message": "Набор стикеров не найден", "code": "pack_not_found"},
        )

    stickers = [
        StickerResponse(
            id=uuid.uuid4(),
            pack_id=pack_id,
            emoji=s["emoji"],
            file_url=s["file_url"],
            is_animated=s["is_animated"],
        )
        for s in pack["stickers"]
    ]

    return StickerPackDetailResponse(
        id=pack_id,
        name=pack["name"],
        description=pack["description"],
        cover_url=pack["cover_url"],
        is_animated=pack["is_animated"],
        is_official=pack["is_official"],
        author_id=uuid.UUID(pack["author_id"]),
        stickers=stickers,
        created_at=datetime.now(),
    )


@router.get("/recent", response_model=RecentStickersResponse)
async def get_recent_stickers(
    limit: int = Query(20, ge=1, le=50),
    current_user: User = Depends(get_current_user),
) -> RecentStickersResponse:
    """Получить недавно использованные стикеры."""
    stickers = [
        StickerResponse(
            id=uuid.uuid4(),
            pack_id=uuid.UUID(DEMO_STICKER_PACKS[0]["id"]),
            emoji="😺",
            file_url="/stickers/cats/1.webp",
            is_animated=False,
        )
    ]
    return RecentStickersResponse(stickers=stickers[:limit])


@router.post("/packs/{pack_id}/add", status_code=status.HTTP_204_NO_CONTENT)
async def add_sticker_pack(
    pack_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
) -> None:
    """Добавить набор стикеров в коллекцию пользователя."""
    pack = next((p for p in DEMO_STICKER_PACKS if p["id"] == str(pack_id)), None)
    if not pack:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"message": "Набор стикеров не найден", "code": "pack_not_found"},
        )


@router.delete("/packs/{pack_id}/remove", status_code=status.HTTP_204_NO_CONTENT)
async def remove_sticker_pack(
    pack_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
) -> None:
    """Удалить набор стикеров из коллекции пользователя."""
    pass


@router.get("/search", response_model=UserStickerPacksResponse)
async def search_sticker_packs(
    query: str = Query(..., min_length=1, max_length=100),
    current_user: User = Depends(get_current_user),
) -> UserStickerPacksResponse:
    """Поиск наборов стикеров."""
    query_lower = query.lower()
    matching_packs = [
        p for p in DEMO_STICKER_PACKS
        if query_lower in p["name"].lower() or (p["description"] and query_lower in p["description"].lower())
    ]

    packs = [
        StickerPackResponse(
            id=uuid.UUID(p["id"]),
            name=p["name"],
            description=p["description"],
            cover_url=p["cover_url"],
            is_animated=p["is_animated"],
            sticker_count=p["sticker_count"],
            author_id=uuid.UUID(p["author_id"]),
            is_official=p["is_official"],
            created_at=datetime.now(),
        )
        for p in matching_packs
    ]
    return UserStickerPacksResponse(packs=packs, total=len(packs))


@router.get("/gifs/search", response_model=GifSearchResponse)
async def search_gifs(
    query: str = Query(..., min_length=1, max_length=100),
    limit: int = Query(20, ge=1, le=50),
    offset: int = Query(0, ge=0),
    current_user: User = Depends(get_current_user),
) -> GifSearchResponse:
    """Поиск GIF (заглушка, в реальности использовать Giphy/Tenor API)."""
    gifs = [
        GifResponse(
            id=g["id"],
            title=g["title"],
            url=g["url"],
            preview_url=g["preview_url"],
            width=g["width"],
            height=g["height"],
        )
        for g in DEMO_GIFS
    ]
    return GifSearchResponse(
        gifs=gifs[offset:offset + limit],
        total=len(gifs),
        next_offset=offset + limit if offset + limit < len(gifs) else None,
    )


@router.get("/gifs/trending", response_model=TrendingGifsResponse)
async def get_trending_gifs(
    limit: int = Query(20, ge=1, le=50),
    current_user: User = Depends(get_current_user),
) -> TrendingGifsResponse:
    """Получить популярные GIF (заглушка)."""
    gifs = [
        GifResponse(
            id=g["id"],
            title=g["title"],
            url=g["url"],
            preview_url=g["preview_url"],
            width=g["width"],
            height=g["height"],
        )
        for g in DEMO_GIFS[:limit]
    ]
    return TrendingGifsResponse(gifs=gifs)
