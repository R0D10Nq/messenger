"""Главный роутер API."""

from fastapi import APIRouter

from src.api.health import router as health_router

router = APIRouter()

router.include_router(health_router, tags=["health"])
