from uuid import UUID

from pydantic import BaseModel, EmailStr

# Properties to receive via API on creation
class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserOut(BaseModel):
    id: UUID
    email: EmailStr

    class Config:
        orm_mode = True


class UserUpdate(BaseModel):
    email: EmailStr


# class UserInDB(BaseModel):
#     id: UUID | None = None
#     email: str
#     hashed_password: str

#     class Config:
#         orm_mode = True


class PermissionCreate(BaseModel):
    name: str


class PermissionOut(BaseModel):
    id: UUID
    name: str

    class Config:
        orm_mode = True


class RoleCreate(BaseModel):
    name: str


class RoleOut(BaseModel):
    id: UUID
    name: str

    class Config:
        orm_mode = True


class RoleHasPermission(BaseModel):
    role_id: UUID
    permission_id: UUID

    class Config:
        orm_mode = True


class RoleHasPermissionUpdate(BaseModel):
    old_permission_id: UUID
    new_permission_id: UUID
