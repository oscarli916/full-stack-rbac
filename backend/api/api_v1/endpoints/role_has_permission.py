from typing import Any
from uuid import UUID

from fastapi import APIRouter, Depends, Header
from sqlalchemy.orm import Session

from api.deps import get_db
import crud
from schemas.rbac import RoleHasPermission
from utils.exception import UvicornException
from utils.security import verify_permission


router = APIRouter()


@router.post("", response_model=RoleHasPermission, status_code=201)
async def create_role_has_permission(
    role_has_permission: RoleHasPermission,
    authorization: str | None = Header(default=None),
    db: Session = Depends(get_db),
) -> Any:
    await verify_permission(db, authorization, permissions=["setting.create"])
    if crud.rbac.get_role_by_id(db, role_id=role_has_permission.role_id) is None:
        raise UvicornException(
            status_code=404,
            message="role not found",
            error=f"role id: {role_has_permission.role_id}",
        )
    if (
        crud.rbac.get_permission_by_id(
            db, permission_id=role_has_permission.permission_id
        )
        is None
    ):
        raise UvicornException(
            status_code=404,
            message="permission not found",
            error=f"permission id: {role_has_permission.permission_id}",
        )
    db_obj = crud.rbac.get_role_has_permission_by_role_id_and_permission_id(
        db,
        role_id=role_has_permission.role_id,
        permission_id=role_has_permission.permission_id,
    )
    if db_obj:
        raise UvicornException(
            status_code=400,
            message="role has permission has already been created",
            error=f"role id: {db_obj.role_id}, permission id: {db_obj.permission_id}",
        )
    return crud.rbac.create_role_has_permission(
        db,
        role_id=role_has_permission.role_id,
        permission_ids=[role_has_permission.permission_id],
    )[0]
