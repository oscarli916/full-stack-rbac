from uuid import UUID

from sqlalchemy.orm import Session

from models.rbac import Role, User, UserHasRole
from schemas.rbac import UserCreate
from utils.security import get_password_hash


class CRUDRbac:
    def create_user(self, db: Session, obj_in: UserCreate) -> User:
        db_obj = User(
            email=obj_in.email, hashed_password=get_password_hash(obj_in.password)
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_role_by_name(self, db: Session, name: str) -> Role:
        return db.query(Role).filter(Role.name == name).first()

    def create_role(self, db: Session, role_name: str) -> Role:
        db_obj = Role(name=role_name)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def create_user_has_role(
        self, db: Session, user_id: UUID, role_id: UUID
    ) -> UserHasRole:
        db_obj = UserHasRole(user_id=user_id, role_id=role_id)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj


rbac = CRUDRbac()
