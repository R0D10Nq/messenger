"""Главный роутер API."""

from fastapi import APIRouter

from src.api.auth import router as auth_router
from src.api.health import router as health_router
from src.api.profile import router as profile_router

router = APIRouter()

router.include_router(health_router, tags=["health"])
router.include_router(auth_router)
router.include_router(profile_router)
