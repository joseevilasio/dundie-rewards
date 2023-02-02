import pytest

from dundie.core import read
from dundie.database import get_session
from dundie.models import Person
from dundie.utils.db import add_person


@pytest.mark.unit
def test_read_with_query():
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

        response = read()
        assert len(response) == 2

        response = read(dept="Management")
        assert len(response) == 1
        assert response[0]["name"] == "Jim Doe"

        response = read(email="joe@doe.com")
        assert len(response) == 1
        assert response[0]["name"] == "Joe Doe"
