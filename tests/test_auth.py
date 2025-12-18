from uuid import uuid4

from fastapi.testclient import TestClient

from src.app.core.config import settings


def test_register_and_login(client: TestClient) -> None:
    email = f"user_{uuid4().hex}@example.com"
    password = "secret123"

    register_payload = {
        "email": email,
        "full_name": "Test User",
        "password": password,
    }

    r = client.post("/api/v1/auth/register", json=register_payload)
    assert r.status_code == 201, r.text
    data = r.json()
    assert data["email"] == email

    login_payload = {"email": email, "password": password}

    r = client.post("/api/v1/auth/login", json=login_payload)
    assert r.status_code == 200, r.text

    data = r.json()
    assert "access_token" in data
    assert data.get("token_type") == "bearer"

    assert settings.COOKIE_NAME in r.cookies
