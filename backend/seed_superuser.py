import logging
import sys
from uuid import UUID

from sqlalchemy.orm import Session

import crud
from db.session import SessionLocal
from schemas.rbac import UserCreate

logging.basicConfig(
    level=logging.INFO,
    format='{"time": "%(asctime)s", "level": "%(levelname)s", "message": "%(message)s"}',
    datefmt="%Y-%m-%d %H:%M:%S",
)


def seed_superuser(db: Session, email: str, password: str) -> UUID:
    logging.info("Seeding super user")
    admin = UserCreate(email=email, password=password)
    db_obj = crud.rbac.create_user(db, obj_in=admin)
    logging.info("Super user has been seeded")
    return db_obj.id


def seed_admin_role(db: Session) -> UUID:
    role = crud.rbac.get_role_by_name(db, "admin")
    if not role:
        logging.info("Seeding admin role")
        admin_role = crud.rbac.create_role(db, role_name="admin")
        logging.info("Admin role has been seeded")
        return admin_role.id
    return role.id


def map_user_role(db: Session, user_id: UUID, role_id: UUID) -> None:
    logging.info("Mapping super user with admin role")
    crud.rbac.create_user_has_role(db, user_id=user_id, role_id=role_id)
    logging.info("Super user and admin role has been mapped")


def main(email: str, password: str) -> None:
    logging.info("Start seeding")
    db = SessionLocal()
    user_id = seed_superuser(db, email, password)
    role_id = seed_admin_role(db)
    map_user_role(db, user_id=user_id, role_id=role_id)
    logging.info("Finish seeding")


if __name__ == "__main__":
    email, password = sys.argv[1], sys.argv[2]
    main(email, password)
