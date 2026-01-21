"""Главный роутер API."""

from fastapi import APIRouter

from src.api.auth import router as auth_router
from src.api.call import router as call_router
from src.api.chat import router as chat_router
from src.api.encryption import router as encryption_router
from src.api.health import router as health_router
from src.api.media import router as media_router
from src.api.profile import router as profile_router
from src.api.reaction import router as reaction_router
from src.api.search import router as search_router
from src.api.totp import router as totp_router
from src.api.transcription import router as transcription_router
from src.api.voice import router as voice_router
from src.api.sticker import router as sticker_router
from src.api.export import router as export_router
from src.api.translate import router as translate_router

router = APIRouter()

router.include_router(health_router, tags=["health"])
router.include_router(auth_router)
router.include_router(profile_router)
router.include_router(chat_router)
router.include_router(media_router)
router.include_router(transcription_router)
router.include_router(totp_router)
router.include_router(encryption_router)
router.include_router(call_router)
router.include_router(reaction_router)
router.include_router(search_router)
router.include_router(voice_router)
router.include_router(sticker_router)
router.include_router(export_router)
router.include_router(translate_router)
