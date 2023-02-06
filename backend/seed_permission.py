import logging
import sys
from uuid import UUID

from sqlalchemy.orm import Session

import crud
from db.session import SessionLocal


logging.basicConfig(
    level=logging.INFO,
    format='{"time": "%(asctime)s", "level": "%(levelname)s", "message": "%(message)s"}',
    datefmt="%Y-%m-%d %H:%M:%S",
)


def seed_permissions(db: Session, permissions: list[str]) -> list[UUID]:
    logging.info("Seeding permissions")
    db_objs = crud.rbac.create_permissions(db, permissions=permissions)
    logging.info("Permissions has been seeded")
    return [obj.id for obj in db_objs]


def map_role_permission(db: Session, permission_ids: list[UUID]) -> None:
    logging.info("Mapping admin role with permissions")
    role = crud.rbac.get_role_by_name(db, "admin")
    crud.rbac.create_role_has_permission(
        db, role_id=role.id, permission_ids=permission_ids
    )
    logging.info("Admin role and permissions has been mapped")


def main(permissions: list[str]) -> None:
    logging.info("Start seeding")
    db = SessionLocal()
    permission_ids = seed_permissions(db, permissions=permissions)
    map_role_permission(db, permission_ids=permission_ids)
    logging.info("Finish seeding")


if __name__ == "__main__":
    permissions = sys.argv[1:]
    main(permissions)
