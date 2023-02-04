import logging

import crud
from db.session import SessionLocal
from schemas.rbac import UserCreate

logging.basicConfig(level=logging.INFO)


def seed_user():
    db = SessionLocal()
    admin = UserCreate(email="admin@test.com", password="12345678")
    manager = UserCreate(email="manager1@test.com", password="12345678")
    senior = UserCreate(email="senior1@test.com", password="12345678")
    test = UserCreate(email="test1@test.com", password="12345678")

    for user in [admin, manager, senior, test]:
        crud.rbac.create_user(db, obj_in=user)


def main():
    logging.info("Seeding user data")
    seed_user()
    logging.info("User data has been seeded")


if __name__ == "__main__":
    main()
