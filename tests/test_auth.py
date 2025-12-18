from fastapi.testclient import TestClient


def test_register_and_login(client: TestClient):
    payload = {
        "email": "user@example.com",
        "full_name": "Test User",
        "password": "secret123",
    }
    r = client.post("/api/v1/auth/register", json=payload)
    assert r.status_code == 201
    data = r.json()
    assert data["email"] == payload["email"]

    login_payload = {"email": payload["email"], "password": payload["password"]}
    r = client.post("/api/v1/auth/login", json=login_payload)
    assert r.status_code == 200
    assert "access_token" in r.json()
    assert "set-cookie" in r.headers.lower()
