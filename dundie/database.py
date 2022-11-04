import json
from dundie.settings import DATABASE_PATH


EMPTY_DB = {"people": {}, "balence": {}, "movement": {}, "users": {}}


def connect():
    """Connect to the database, returns dict data."""
    try:
        with open(DATABASE_PATH, "r") as database_file:
            return json.loads(database_file.read())
    except (json.JSONDecodeError, FileNotFoundError):
        return EMPTY_DB


def commit(db):
    """Sabe database back to the database file."""
    if db.keys() != EMPTY_DB.keys():
        raise RuntimeError("Database schema is invalid.")
    with open(DATABASE_PATH, "w") as database_file:
        database_file.write(json.dumps(db, indent=4))


def add_person(db, pk, data):
    """Saves person data to database.
    - Email is unique (resolved by dictionary hash table)
    - If exists, update, else create
    - Set initial balance (managers = 100, others = 500)
    - Generate a password if user is new and send_email
    """
    pass
