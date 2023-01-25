import getpass
import os

from sqlmodel import select

from dundie.database import get_session
from dundie.models import InvalidEmailError, Person, User
from dundie.utils.email import check_valid_email


class InvalidPasswordError(Exception):
    ...


class UserNotFoundError(Exception):
    ...


class AuthenticationError(Exception):
    ...


def validation_user_if_exist(user: str) -> bool:
    """Validation User if exist in database"""

    if not check_valid_email(user):
        raise InvalidEmailError(f"Invalid email for {user!r}")

    with get_session() as session:

        instance = session.exec(
            select(Person.email).where(Person.email == user)
        ).first()

        if instance:
            return True
        if not instance:
            raise UserNotFoundError(f"User not found: {user!r}")


def validation_password(user: str, password: str) -> bool:
    """Ensure password is correct"""

    with get_session() as session:

        instance = session.exec(
            select(User.password).where(Person.email == user)
        ).first()

        if instance == password:
            return True
        else:
            raise InvalidPasswordError(f"Invalid password for {user!r}")


def require_password() -> bool:
    """Input user and password"""

    user = input(str("User: "))

    os.environ["DUNDER_USER"] = user

    if validation_user_if_exist(user):
        password = getpass.getpass()
        if validation_password(user, password):
            return True

    else:
        return False
