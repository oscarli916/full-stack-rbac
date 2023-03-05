from typing import Any

from fastapi import APIRouter, Depends, Header
from sqlalchemy.orm import Session

from api.deps import get_db
import crud
from schemas.rbac import PermissionCreate, PermissionOut
from utils.exception import UvicornException
from utils.security import verify_permission


router = APIRouter()


@router.post("/permission", response_model=PermissionOut, status_code=201)
async def create_permission(
    permission: PermissionCreate,
    authorization: str | None = Header(default=None),
    db: Session = Depends(get_db),
) -> Any:
    await verify_permission(db, authorization, permissions=["setting.create"])
    db_obj = crud.rbac.get_permission_by_name(db, name=permission.name)
    if db_obj:
        raise UvicornException(
            status_code=400,
            message="permission has already been created",
            error=f"permission id: {db_obj.id}, permission name: {db_obj.name}",
        )
    return crud.rbac.create_permissions(db, permissions=[permission.name])[0]


@router.get("/permission", response_model=list[PermissionOut], status_code=200)
async def read_permissions(
    authorization: str | None = Header(default=None), db: Session = Depends(get_db)
) -> Any:
    await verify_permission(db, authorization, permissions=["setting.read"])
    return crud.rbac.get_permissions(db)
