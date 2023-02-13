#!/usr/bin/env bash
alembic upgrade head
python seed_superuser.py admin@test.com 12345678
python seed_user.py manager1@test.com 12345678
python seed_user.py senior1@test.com 12345678
python seed_user.py test1@test.com 12345678
python seed_permission.py setting.create setting.read setting.update setting.delete
