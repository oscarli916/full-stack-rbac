from uuid import UUID

from sqlalchemy.orm import Session

from models.rbac import Permission, Role, RoleHasPermission, User, UserHasRole
from schemas.rbac import UserCreate
from utils.security import get_password_hash


class CRUDRbac:
    # User
    def create_user(self, db: Session, obj_in: UserCreate) -> User:
        db_obj = User(
            email=obj_in.email, hashed_password=get_password_hash(obj_in.password)
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    # Role
    def get_role_by_name(self, db: Session, name: str) -> Role:
        return db.query(Role).filter(Role.name == name).first()

    def create_role(self, db: Session, role_name: str) -> Role:
        db_obj = Role(name=role_name)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    # RoleHasPermission
    def create_role_has_permission(
        self, db: Session, role_id: UUID, permission_ids: list[UUID]
    ) -> list[RoleHasPermission]:
        db_objs = [
            RoleHasPermission(role_id=role_id, permission_id=permission_id)
            for permission_id in permission_ids
        ]
        db.add_all(db_objs)
        db.commit()
        return db_objs

    # UserHasRole
    def create_user_has_role(
        self, db: Session, user_id: UUID, role_id: UUID
    ) -> UserHasRole:
        db_obj = UserHasRole(user_id=user_id, role_id=role_id)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    # Permission
    def create_permissions(
        self, db: Session, permissions: list[str]
    ) -> list[Permission]:
        db_objs = [Permission(name=permission) for permission in permissions]
        db.add_all(db_objs)
        db.commit()
        for db_obj in db_objs:
            db.refresh(db_obj)
        return db_objs


rbac = CRUDRbac()
