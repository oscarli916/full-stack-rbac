from uuid import UUID

from sqlalchemy.orm import Session

from models.rbac import Permission, Role, RoleHasPermission, User, UserHasRole
from schemas.rbac import UserCreate
from utils.security import get_password_hash, verify_password


class CRUDRbac:
    def authenticate(self, db: Session, obj_in: UserCreate) -> User | None:
        user = self.get_user_by_email(db, email=obj_in.email)
        if not user:
            return None
        if not verify_password(
            password=obj_in.password, hashed_password=user.hashed_password
        ):
            return None
        return user

    # User
    def get_user_by_email(self, db: Session, email: str) -> User | None:
        return db.query(User).filter(User.email == email).first()

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
    def get_all_permission_ids_by_role_id(
        self, db: Session, role_id: UUID
    ) -> list[UUID]:
        permission_ids = (
            db.query(RoleHasPermission.permission_id)
            .filter(RoleHasPermission.role_id == role_id)
            .all()
        )
        return [permission_id[0] for permission_id in permission_ids]

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
    def get_all_role_ids_by_user_id(self, db: Session, user_id: UUID) -> list[UUID]:
        role_ids = (
            db.query(UserHasRole.role_id).filter(UserHasRole.user_id == user_id).all()
        )
        return [role_id[0] for role_id in role_ids]

    def create_user_has_role(
        self, db: Session, user_id: UUID, role_id: UUID
    ) -> UserHasRole:
        db_obj = UserHasRole(user_id=user_id, role_id=role_id)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    # Permission
    def get_permission_name_by_id(self, db: Session, permission_id: UUID) -> str:
        return (
            db.query(Permission.name).filter(Permission.id == permission_id).first()[0]
        )

    def get_permission_by_id(
        self, db: Session, permission_id: UUID
    ) -> Permission | None:
        return db.query(Permission).filter(Permission.id == permission_id).first()

    def get_permission_by_name(self, db: Session, name: str) -> Permission | None:
        return db.query(Permission).filter(Permission.name == name).first()

    def get_permissions(self, db: Session) -> list[Permission]:
        return db.query(Permission).all()

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
