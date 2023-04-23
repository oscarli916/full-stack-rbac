from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from api.deps import get_db
import crud
from main import app
from schemas.rbac import UserCreate
from tests.conftest import override_get_db

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


def test_create_user(db: Session) -> None:
    email = "admin@test.com"
    password = "12345678"
    permissions = ["setting.create", "setting.read", "setting.update", "setting.delete"]
    admin = UserCreate(email=email, password=password)
    user = crud.rbac.create_user(db, obj_in=admin)
    role = crud.rbac.create_role(db, role_name="admin")
    crud.rbac.create_user_has_role(db, user_id=user.id, role_id=role.id)
    db_objs = crud.rbac.create_permissions(db, permissions=permissions)
    crud.rbac.create_role_has_permission(
        db, role_id=role.id, permission_ids=[obj.id for obj in db_objs]
    )

    login_data = {"email": email, "password": password}
    r = client.post("/api/v1/auth/login", json=login_data)
    res = r.json()

    new_email = "test@test.com"
    new_password = "12345678"
    header = {"authorization": f"Bearer {res['token']}"}
    r = client.post(
        "/api/v1/rbac/user",
        json={"email": new_email, "password": new_password},
        headers=header,
    )
    res = r.json()
    assert r.status_code == 201
    assert "id" in res
    assert "email" in res
    assert res["email"] == new_email


def test_create_duplicate_user(db: Session) -> None:
    email = "admin@test.com"
    password = "12345678"
    permissions = ["setting.create", "setting.read", "setting.update", "setting.delete"]
    admin = UserCreate(email=email, password=password)
    user = crud.rbac.create_user(db, obj_in=admin)
    role = crud.rbac.create_role(db, role_name="admin")
    crud.rbac.create_user_has_role(db, user_id=user.id, role_id=role.id)
    db_objs = crud.rbac.create_permissions(db, permissions=permissions)
    crud.rbac.create_role_has_permission(
        db, role_id=role.id, permission_ids=[obj.id for obj in db_objs]
    )

    login_data = {"email": email, "password": password}
    r = client.post("/api/v1/auth/login", json=login_data)
    res = r.json()

    new_email = "admin@test.com"
    new_password = "12345678"
    header = {"authorization": f"Bearer {res['token']}"}
    r = client.post(
        "/api/v1/rbac/user",
        json={"email": new_email, "password": new_password},
        headers=header,
    )
    res = r.json()
    assert r.status_code == 400
    assert "message" in res
    assert "error" in res
    assert res["message"] == "user has already been created"
