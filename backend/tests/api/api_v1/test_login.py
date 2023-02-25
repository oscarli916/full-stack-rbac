from fastapi.testclient import TestClient

from main import app


client = TestClient(app)


def test_login_success() -> None:
    login_data = {"email": "admin@test.com", "password": "12345678"}
    r = client.post("/api/v1/login", json=login_data)
    res = r.json()
    assert r.status_code == 200
    assert "permissions" in res
    assert "token" in res
    assert res["token"]


def test_login_wrong_password() -> None:
    login_data = {"email": "admin@test.com", "password": "87654321"}
    r = client.post("/api/v1/login", json=login_data)
    res = r.json()
    assert r.status_code == 400
    assert "message" in res
    assert res["message"] == "Incorrect email or password"


def test_login_invalid_user() -> None:
    login_data = {"email": "invalid@test.com", "password": "87654321"}
    r = client.post("/api/v1/login", json=login_data)
    res = r.json()
    assert r.status_code == 400
    assert "message" in res
    assert res["message"] == "Incorrect email or password"
