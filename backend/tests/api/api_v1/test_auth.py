from fastapi.testclient import TestClient

from main import app


client = TestClient(app)


def test_login_success() -> None:
    login_data = {"email": "admin@test.com", "password": "12345678"}
    r = client.post("/api/v1/auth/login", json=login_data)
    res = r.json()
    assert r.status_code == 201
    assert "permissions" in res
    assert "token" in res
    assert res["token"]


def test_login_wrong_password() -> None:
    login_data = {"email": "admin@test.com", "password": "87654321"}
    r = client.post("/api/v1/auth/login", json=login_data)
    res = r.json()
    assert r.status_code == 400
    assert "message" in res
    assert res["message"] == "Incorrect email or password"


def test_login_invalid_user() -> None:
    login_data = {"email": "invalid@test.com", "password": "87654321"}
    r = client.post("/api/v1/auth/login", json=login_data)
    res = r.json()
    assert r.status_code == 400
    assert "message" in res
    assert res["message"] == "Incorrect email or password"


def test_auth_success_without_permissions() -> None:
    login_data = {"email": "admin@test.com", "password": "12345678"}
    r = client.post("/api/v1/auth/login", json=login_data)
    res = r.json()

    auth_data = {"permissions": [], "token": res["token"]}
    r = client.post("/api/v1/auth", json=auth_data)
    res = r.json()
    assert r.status_code == 201
    assert "message" in res
    assert res["message"] == "success"


def test_auth_success_with_permissions() -> None:
    login_data = {"email": "admin@test.com", "password": "12345678"}
    r = client.post("/api/v1/auth/login", json=login_data)
    res = r.json()

    auth_data = {
        "permissions": [
            "setting.create",
            "setting.read",
            "setting.update",
            "setting.delete",
        ],
        "token": res["token"],
    }
    r = client.post("/api/v1/auth", json=auth_data)
    res = r.json()
    assert r.status_code == 201
    assert "message" in res
    assert res["message"] == "success"


def test_auth_without_permission() -> None:
    login_data = {"email": "admin@test.com", "password": "12345678"}
    r = client.post("/api/v1/auth/login", json=login_data)
    res = r.json()

    auth_data = {
        "permissions": [
            "invalid.create",
        ],
        "token": res["token"],
    }
    r = client.post("/api/v1/auth", json=auth_data)
    res = r.json()
    assert r.status_code == 401
    assert "message" in res
    assert res["message"] == "user does not have permission"


def test_auth_invalid_jwt() -> None:
    auth_data = {
        "permissions": [],
        "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJmdWxsLXN0YWNrLXJiYWMiLCJleHAiOjE2zc0MjY5MzksImlhdCI6MTY3NzMxMTczOSwicGVybWlzc2lvbnMiOlsiYTE0MTczOTItYmJkOS00ZGJlLWFiMDktMGFlNzEyYTE1NzgwIiwiMjhhNzcwYTUtMDFhMC00YzkzLWFkOTQtZWFhNmJhYjliMzhlIiwiYWNhOTBhZmYtMTM1MS00MTU0LWFmMTYtYWM1ZmNjOGY2MDkwIiwiMDJjMzE5ZmEtN2E5Yi00MDg0LWE0N2QtNWI3MGRkOGYzMzhkIl0sImVtYWlsIjoiYWRtaW5AdGVzdC5jb20ifQ.yXqQ7BrN8TNSxieqa-caeXvVnXkWOKKeUmhralfcqt0",
    }
    r = client.post("/api/v1/auth", json=auth_data)
    res = r.json()
    assert r.status_code == 401
    assert "message" in res
    assert res["message"] == "user is not authorized"
