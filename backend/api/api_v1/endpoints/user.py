from typing import Any

from fastapi import APIRouter, Depends, Header
from sqlalchemy.orm import Session

from api.deps import get_db
import crud
from schemas.rbac import UserCreate, UserOut
from utils.exception import UvicornException
from utils.security import verify_permission


router = APIRouter()


@router.post("", response_model=UserOut, status_code=201)
async def create_user(
    user: UserCreate,
    authorization: str | None = Header(default=None),
    db: Session = Depends(get_db),
) -> Any:
    await verify_permission(db, authorization, permissions=["setting.create"])
    db_obj = crud.rbac.get_user_by_email(db, email=user.email)
    if db_obj:
        raise UvicornException(
            status_code=400,
            message="user has already been created",
            error=f"user id: {db_obj.id}, user email: {db_obj.email}",
        )
    return crud.rbac.create_user(db, obj_in=user)
