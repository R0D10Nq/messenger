"""Health check эндпоинты."""

from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()


class HealthResponse(BaseModel):
    """Ответ healthcheck."""

    status: str
    version: str


@router.get("/health", response_model=HealthResponse)
async def health_check() -> HealthResponse:
    """Проверка работоспособности API."""
    return HealthResponse(status="ok", version="0.1.0")
