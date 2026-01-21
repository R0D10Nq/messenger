"""Тесты для стикеров и GIF."""

import uuid

import pytest


class TestStickerSchemas:
    """Тесты схем стикеров."""

    def test_sticker_pack_create(self):
        """StickerPackCreate валидация."""
        from src.schemas.sticker import StickerPackCreate

        data = StickerPackCreate(
            name="Котики",
            description="Милые котики",
            is_animated=False,
        )
        assert data.name == "Котики"
        assert data.description == "Милые котики"
        assert data.is_animated is False

    def test_sticker_pack_create_minimal(self):
        """StickerPackCreate с минимальными данными."""
        from src.schemas.sticker import StickerPackCreate

        data = StickerPackCreate(name="Тест")
        assert data.name == "Тест"
        assert data.description is None
        assert data.is_animated is False

    def test_sticker_create(self):
        """StickerCreate валидация."""
        from src.schemas.sticker import StickerCreate

        pack_id = uuid.uuid4()
        data = StickerCreate(
            pack_id=pack_id,
            emoji="😺",
            file_url="/stickers/cat.webp",
        )
        assert data.pack_id == pack_id
        assert data.emoji == "😺"
        assert data.file_url == "/stickers/cat.webp"

    def test_sticker_response(self):
        """StickerResponse валидация."""
        from src.schemas.sticker import StickerResponse

        data = StickerResponse(
            id=uuid.uuid4(),
            pack_id=uuid.uuid4(),
            emoji="😀",
            file_url="/stickers/smile.webp",
            is_animated=True,
        )
        assert data.emoji == "😀"
        assert data.is_animated is True

    def test_sticker_pack_response(self):
        """StickerPackResponse валидация."""
        from datetime import UTC, datetime

        from src.schemas.sticker import StickerPackResponse

        now = datetime.now(UTC)
        data = StickerPackResponse(
            id=uuid.uuid4(),
            name="Эмоции",
            description="Набор эмоций",
            cover_url="/stickers/emotions/cover.webp",
            is_animated=True,
            sticker_count=10,
            author_id=uuid.uuid4(),
            is_official=True,
            created_at=now,
        )
        assert data.name == "Эмоции"
        assert data.sticker_count == 10
        assert data.is_official is True

    def test_gif_search_request(self):
        """GifSearchRequest валидация."""
        from src.schemas.sticker import GifSearchRequest

        data = GifSearchRequest(query="кот", limit=30, offset=10)
        assert data.query == "кот"
        assert data.limit == 30
        assert data.offset == 10

    def test_gif_search_request_defaults(self):
        """GifSearchRequest с дефолтными значениями."""
        from src.schemas.sticker import GifSearchRequest

        data = GifSearchRequest(query="собака")
        assert data.query == "собака"
        assert data.limit == 20
        assert data.offset == 0

    def test_gif_response(self):
        """GifResponse валидация."""
        from src.schemas.sticker import GifResponse

        data = GifResponse(
            id="gif123",
            title="Танцующий кот",
            url="https://giphy.com/cat.gif",
            preview_url="https://giphy.com/cat_s.gif",
            width=200,
            height=150,
        )
        assert data.id == "gif123"
        assert data.title == "Танцующий кот"
        assert data.width == 200

    def test_gif_search_response(self):
        """GifSearchResponse валидация."""
        from src.schemas.sticker import GifResponse, GifSearchResponse

        gif = GifResponse(
            id="gif1",
            title="Тест",
            url="https://test.gif",
            preview_url="https://test_s.gif",
            width=100,
            height=100,
        )
        data = GifSearchResponse(gifs=[gif], total=1, next_offset=None)
        assert len(data.gifs) == 1
        assert data.total == 1
        assert data.next_offset is None

    def test_user_sticker_packs_response(self):
        """UserStickerPacksResponse валидация."""
        from src.schemas.sticker import UserStickerPacksResponse

        data = UserStickerPacksResponse(packs=[], total=0)
        assert data.packs == []
        assert data.total == 0

    def test_recent_stickers_response(self):
        """RecentStickersResponse валидация."""
        from src.schemas.sticker import RecentStickersResponse

        data = RecentStickersResponse(stickers=[])
        assert data.stickers == []
