from sqlalchemy.orm import Session

from models.rbac import User
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


rbac = CRUDRbac()
