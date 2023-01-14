import pytest

from dundie.database import get_session
from dundie.models import InvalidEmailError, Person
from dundie.utils.db import add_person
from dundie.utils.email import check_valid_email
from dundie.utils.login import validation_user_if_exist
from dundie.utils.user import generate_simple_password


@pytest.mark.unit
@pytest.mark.medium
@pytest.mark.parametrize(
    "address", ["jose@gmail.com", "joe@doe.com", "a@b.pt"]
)
def test_positive_check_valid_email(address):
    """Ensure email is valid."""
    assert check_valid_email(address) is True


@pytest.mark.unit
@pytest.mark.medium
@pytest.mark.parametrize("address", ["jose@.com", "@doe.com", "a@b"])
def test_negative_check_valid_email(address):
    """Ensure email is invalid."""
    assert check_valid_email(address) is False


@pytest.mark.unit
@pytest.mark.medium
def test_generate_simple_password():
    """Test generation of random simple password.
    TODO: Generate hashed complex passwords, encrypit it
    """
    passwords = []
    for _ in range(100):
        passwords.append(generate_simple_password(8))

    assert len(set(passwords)) == 100


@pytest.mark.unit
@pytest.mark.parametrize("user", ["joe@doe.com", "jim@doe.com"])
def test_positive_validation_user_if_exist(user):
    """Ensure user is valid"""
    with get_session() as session:

        joe = {
            "email": "joe@doe.com",
            "name": "Joe Doe",
            "dept": "Sales",
            "role": "Salesman",
        }

        instance_joe = Person(**joe)
        _, created = add_person(session=session, instance=instance_joe)
        assert created is True

        jim = {
            "email": "jim@doe.com",
            "name": "Jim Doe",
            "dept": "Management",
            "role": "Manager",
        }

        instance_jim = Person(**jim)
        _, created = add_person(session=session, instance=instance_jim)
        assert created is True

        session.commit()

        assert validation_user_if_exist(user) is True


@pytest.mark.unit
@pytest.mark.parametrize("user", ["flavio@doe.com", "jose@doe.com"])
def test_negative_validation_user_if_exist(user):
    """Ensure user is valid"""
    with pytest.raises(InvalidEmailError):
        with get_session() as session:

            joe = {
                "email": "joe@doe.com",
                "name": "Joe Doe",
                "dept": "Sales",
                "role": "Salesman",
            }

            instance_joe = Person(**joe)
            _, created = add_person(session=session, instance=instance_joe)
            assert created is True

            jim = {
                "email": "jim@doe.com",
                "name": "Jim Doe",
                "dept": "Management",
                "role": "Manager",
            }

            instance_jim = Person(**jim)
            _, created = add_person(session=session, instance=instance_jim)
            assert created is True

            session.commit()

            validation_user_if_exist(user)
