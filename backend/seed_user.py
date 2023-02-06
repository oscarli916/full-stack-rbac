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


def seed_user(db: Session, email: str, password: str) -> UUID:
    logging.info("Seeding normal user")
    user = UserCreate(email=email, password=password)
    crud.rbac.create_user(db, obj_in=user)
    logging.info("Normal user has been seeded")


def main(email: str, password: str) -> None:
    logging.info("Start seeding")
    db = SessionLocal()
    seed_user(db, email, password)
    logging.info("Finish seeding")


if __name__ == "__main__":
    email, password = sys.argv[1], sys.argv[2]
    main(email, password)
