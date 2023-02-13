# Full Stack RBAC Application

## Start Application

`docker compose up`

## Backend

Change `psycopg2==2.9.5` -> `psycopg2-binary==2.9.5` in `requirements.txt` in order to work on Linux

### Seeding

Default data will be seeded automatically

-   #### Super User

    To seed super user. Run the following command:

    `python seed_superuser.py <email> <password>`

-   #### Normal User

    To seed normal user. Run the following command:

    `python seed_user.py <email> <password>`

-   #### Permission

    To seed permissions. Run the following command:

    `python seed_permission.py [<permission1>]`

### FAQ

-   #### `/usr/bin/env: ‘bash\r’: No such file or directory` during docker compose:

    Make sure all the `.sh` files are using `LF` for End of Line Sequence

## Frontend
