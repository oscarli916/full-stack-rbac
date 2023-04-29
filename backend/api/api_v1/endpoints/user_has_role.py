from typing import Any
from uuid import UUID

from fastapi import APIRouter, Depends, Header
from sqlalchemy.orm import Session

from api.deps import get_db
import crud
from schemas.rbac import UserHasRole
from utils.exception import UvicornException
from utils.security import verify_permission


router = APIRouter()


@router.post("", response_model=UserHasRole, status_code=201)
async def create_user_has_role(
    user_has_role: UserHasRole,
    authorization: str | None = Header(default=None),
    db: Session = Depends(get_db),
) -> Any:
    await verify_permission(db, authorization, permissions=["setting.create"])
    if crud.rbac.get_user_by_id(db, user_id=user_has_role.user_id) is None:
        raise UvicornException(
            status_code=404,
            message="user not found",
            error=f"no user id: {user_has_role.user_id}",
        )
    if crud.rbac.get_role_by_id(db, role_id=user_has_role.role_id) is None:
        raise UvicornException(
            status_code=404,
            message="role not found",
            error=f"no role id: {user_has_role.role_id}",
        )
    db_obj = crud.rbac.get_user_has_permission_by_user_id_and_role_id(
        db,
        user_id=user_has_role.user_id,
        role_id=user_has_role.role_id,
    )
    if db_obj:
        raise UvicornException(
            status_code=400,
            message="user has role has already been created",
            error=f"user id: {db_obj.user_id}, role id: {db_obj.role_id}",
        )
    return crud.rbac.create_user_has_role(
        db,
        user_id=user_has_role.user_id,
        role_id=user_has_role.role_id,
    )
