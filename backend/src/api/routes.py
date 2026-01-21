"""Главный роутер API."""

from fastapi import APIRouter

from src.api.auth import router as auth_router
from src.api.chat import router as chat_router
from src.api.health import router as health_router
from src.api.media import router as media_router
from src.api.profile import router as profile_router
from src.api.totp import router as totp_router
from src.api.transcription import router as transcription_router

router = APIRouter()

router.include_router(health_router, tags=["health"])
router.include_router(auth_router)
router.include_router(profile_router)
router.include_router(chat_router)
router.include_router(media_router)
router.include_router(transcription_router)
router.include_router(totp_router)
