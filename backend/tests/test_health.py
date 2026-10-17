from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health_check_returns_ok() -> None:
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_api_cors_allows_any_origin_with_credentials() -> None:
    allowed = client.options(
        "/auth/me",
        headers={
            "Origin": "https://untrusted.example",
            "Access-Control-Request-Method": "PUT",
            "Access-Control-Request-Headers": "authorization, x-custom-header",
        },
    )

    assert allowed.status_code == 200
    assert allowed.headers["access-control-allow-origin"] == "https://untrusted.example"
    assert allowed.headers["access-control-allow-credentials"] == "true"
    assert "PUT" in allowed.headers["access-control-allow-methods"]
    assert "x-custom-header" in allowed.headers["access-control-allow-headers"]
