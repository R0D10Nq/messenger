"""Фикстуры pytest для тестов."""

import pytest
from fastapi.testclient import TestClient

from src.main import app


@pytest.fixture
def client() -> TestClient:
    """Тестовый клиент FastAPI."""
    return TestClient(app)
