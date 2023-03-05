from datetime import datetime, timedelta, timezone
import os
from typing import Any
from uuid import UUID

import bcrypt
import jwt
from sqlalchemy.orm import Session

from api.api_v1.endpoints import auth
from schemas.token import Token
from utils.exception import UvicornException


def get_password_hash(password: str) -> str:
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode()


def verify_password(password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(password.encode("utf-8"), hashed_password.encode("utf-8"))


def generate_jwt(permission_ids: list[UUID], email: str) -> str:
    permission_ids = [str(permission_id) for permission_id in permission_ids]
    payload = {
        "iss": "full-stack-rbac",
        "exp": datetime.now(tz=timezone.utc) + timedelta(days=1),
        "iat": datetime.now(tz=timezone.utc),
        "permissions": permission_ids,
        "email": email,
    }
    return jwt.encode(
        payload,
        os.getenv("SECRET_KEY"),
        algorithm="HS256",
    )


def verify_jwt(token: str) -> dict[str, Any]:
    try:
        return jwt.decode(
            token,
            os.getenv("SECRET_KEY"),
            algorithms=["HS256"],
            issuer="full-stack-rbac",
        )
    except Exception as e:
        raise UvicornException(
            status_code=401,
            message="user is not authorized",
            error=str(e),
        )


async def verify_permission(
    db: Session, authorization: str | None, permissions: list[str]
) -> bool:
    if not authorization.startswith("Bearer "):
        raise UvicornException(
            status_code=401,
            message="user is not authorized",
            error="header does not start with Bearer",
        )
    token = authorization.split("Bearer ")[1]
    res = await auth.auth(Token(permissions=permissions, token=token), db=db)
    if res.status_code == 401:
        raise UvicornException(
            status_code=401,
            message="user is not authorized",
            error="user does not have permission",
        )
    return True
