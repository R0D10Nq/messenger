"""Тесты health check эндпоинта."""

from fastapi.testclient import TestClient


def test_health_check_returns_ok(client: TestClient) -> None:
    """Health check должен возвращать status=ok."""
    response = client.get("/api/health")

    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert "version" in data


def test_health_check_returns_version(client: TestClient) -> None:
    """Health check должен возвращать версию API."""
    response = client.get("/api/health")

    assert response.status_code == 200
    data = response.json()
    assert data["version"] == "0.1.0"
