from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health_check_returns_ok() -> None:
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_api_cors_allows_any_origin_with_credentials() -> None:
    allowed_origin = client.options(
        "/auth/me",
        headers={
            "Origin": "https://untrusted.example",
            "Access-Control-Request-Method": "POST",
            "Access-Control-Request-Headers": "authorization, content-type",
        },
    )

    assert allowed_origin.status_code == 200
    assert allowed_origin.headers["access-control-allow-origin"] in (
        "*",
        "https://untrusted.example",
    )
    assert allowed_origin.headers["access-control-allow-credentials"] == "true"
    assert "POST" in allowed_origin.headers["access-control-allow-methods"]
    assert "authorization" in allowed_origin.headers["access-control-allow-headers"]
