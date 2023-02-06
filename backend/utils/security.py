from datetime import datetime, timedelta
import os
from uuid import UUID

import bcrypt
import jwt


def get_password_hash(password: str) -> str:
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode()


def verify_password(password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(password.encode("utf-8"), hashed_password.encode("utf-8"))


def generate_jwt(permission_ids: list[UUID], email: str) -> str:
    permission_ids = [str(permission_id) for permission_id in permission_ids]
    payload = {
        "iss": "full-stack-rbac",
        "exp": datetime.now() + timedelta(days=1),
        "iat": datetime.now(),
        "permissions": permission_ids,
        "email": email,
    }
    return jwt.encode(
        payload,
        os.getenv("SECRET_KEY"),
        algorithm="HS256",
    )
