from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health_check_returns_ok() -> None:
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_api_cors_allows_configured_origins_and_rejects_unknown_origin() -> None:
    allowed_frontend = client.options(
        "/auth/me",
        headers={
            "Origin": "https://job-tracker-m6s6.vercel.app",
            "Access-Control-Request-Method": "POST",
            "Access-Control-Request-Headers": "authorization, content-type",
        },
    )
    allowed_local = client.options(
        "/auth/me",
        headers={
            "Origin": "http://localhost:5173",
            "Access-Control-Request-Method": "GET",
            "Access-Control-Request-Headers": "authorization",
        },
    )
    denied = client.options(
        "/auth/me",
        headers={
            "Origin": "https://untrusted.example",
            "Access-Control-Request-Method": "POST",
            "Access-Control-Request-Headers": "authorization",
        },
    )

    assert allowed_frontend.status_code == 200
    assert (
        allowed_frontend.headers["access-control-allow-origin"]
        == "https://job-tracker-m6s6.vercel.app"
    )
    assert allowed_frontend.headers["access-control-allow-credentials"] == "true"
    assert allowed_local.status_code == 200
    assert allowed_local.headers["access-control-allow-origin"] == "http://localhost:5173"
    assert denied.status_code == 400
    assert "access-control-allow-origin" not in denied.headers
