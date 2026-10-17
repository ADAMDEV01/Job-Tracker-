from collections.abc import Generator

from fastapi.testclient import TestClient
from sqlalchemy.exc import OperationalError

from app.db.database import get_db


def test_health_check_returns_ok(client: TestClient) -> None:
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_readiness_check_returns_ready(client: TestClient) -> None:
    response = client.get("/health/ready")

    assert response.status_code == 200
    assert response.json() == {"status": "ready"}


def test_database_errors_are_cors_accessible(
    client: TestClient,
) -> None:
    def unavailable_database() -> Generator[None, None, None]:
        raise OperationalError("SELECT", {}, RuntimeError("database unavailable"))
        yield

    client.app.dependency_overrides[get_db] = unavailable_database
    response = client.get(
        "/health/ready",
        headers={"Origin": "https://job-tracker-m6s6.vercel.app"},
    )

    assert response.status_code == 503
    assert response.json() == {
        "detail": "Database unavailable. Verify DATABASE_URL and apply Alembic migrations."
    }
    assert (
        response.headers["access-control-allow-origin"]
        == "https://job-tracker-m6s6.vercel.app"
    )


def test_api_cors_allows_any_origin_with_credentials(client: TestClient) -> None:
    allowed_origin = client.options(
        "/auth/me",
        headers={
            "Origin": "https://untrusted.example",
            "Access-Control-Request-Method": "POST",
            "Access-Control-Request-Headers": "authorization, content-type",
        },
    )

    assert allowed_origin.status_code == 200
    assert allowed_origin.headers["access-control-allow-origin"] == "https://untrusted.example"
    assert allowed_origin.headers["access-control-allow-credentials"] == "true"
    assert "POST" in allowed_origin.headers["access-control-allow-methods"]
    assert "authorization" in allowed_origin.headers["access-control-allow-headers"]
