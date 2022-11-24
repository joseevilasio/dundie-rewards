import pytest

from dundie.database import connect, commit, add_person
from dundie.core import add


@pytest.mark.unit
@pytest.mark.low
def test_add_movement():
    db = connect()

    pk = "joe@doe.com"
    data = {"role": "Salesman", "dept": "Sales", "name": "Joe Doe"}
    _, created = add_person(db, pk, data)
    assert created is True

    pk = "jim@doe.com"
    data = {"role": "Manager", "dept": "Management", "name": "Jim Doe"}
    _, created = add_person(db, pk, data)
    assert created is True

    commit(db)

    add(-30, email="joe@doe.com")
    add(90, dept="Management")

    db = connect()
    assert db["balance"]["joe@doe.com"] == 470
    assert db["balance"]["jim@doe.com"] == 190
