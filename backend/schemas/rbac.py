from uuid import UUID

from pydantic import BaseModel, EmailStr

# Properties to receive via API on creation
class UserCreate(BaseModel):
    email: EmailStr
    password: str


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
