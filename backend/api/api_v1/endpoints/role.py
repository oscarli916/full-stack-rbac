from typing import Any

from fastapi import APIRouter, Depends, Header
from sqlalchemy.orm import Session

from api.deps import get_db
import crud
from schemas.rbac import RoleCreate, RoleOut
from utils.exception import UvicornException
from utils.security import verify_permission


router = APIRouter()


@router.post("", response_model=RoleOut, status_code=201)
async def create_role(
    role: RoleCreate,
    authorization: str | None = Header(default=None),
    db: Session = Depends(get_db),
) -> Any:
    await verify_permission(db, authorization, permissions=["setting.create"])
    db_obj = crud.rbac.get_role_by_name(db, name=role.name)
    if db_obj:
        raise UvicornException(
            status_code=400,
            message="role has already been created",
            error=f"role id: {db_obj.id}, role name: {db_obj.name}",
        )
    return crud.rbac.create_role(db, role_name=role.name)
