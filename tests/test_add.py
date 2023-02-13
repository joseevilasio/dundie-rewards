import pytest

from dundie.core import add
from dundie.database import get_session
from dundie.models import Person
from dundie.utils.db import add_person


@pytest.mark.unit
def test_add_movement():
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

        add(-30, email="joe@doe.com")
        add(90, dept="Management")

        assert instance_joe.balance[0].value == 470
        assert instance_jim.balance[0].value == 190


@pytest.mark.unit
def test_add_movement_negative_query_empty():
    with pytest.raises(RuntimeError):
        add(-30, email="joe@doe.com")
        add(90, dept="Management")
