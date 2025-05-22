from unittest import mock
import pytest
from mock_alchemy.mocking import UnifiedAlchemyMagicMock
from sqlalchemy.orm.exc import NoResultFound
from src.models.sqlite.entities.people import PeopleTable
from .people_repository import PeopleRepository

class MockConnection:
    def __init__(self) -> None:
        self.session = UnifiedAlchemyMagicMock(
            data = [
                (
                    [mock.call.query(PeopleTable)],
                    [
                        PeopleTable(
                            id=1,
                            first_name="Felipe",
                            last_name="Viana de Andrade",
                            age=40,
                            pet_id=1
                        ),
                         PeopleTable(
                            id=2,
                            first_name="Priscila",
                            last_name="O M Andrade",
                            age=38,
                            pet_id=2
                        )
                    ]
                )
            ]
        )

    def __enter__(self): return self
    def __exit__(self, exc_type, exc_val, exc_tb): pass

class MockConnectionNoResult:
    def __init__(self) -> None:
        self.session = UnifiedAlchemyMagicMock()
        self.session.query.side_effect = self.__raise_no_result_found
        self.session.add.side_effect = self.__raise_no_result_found

    def __raise_no_result_found(self, *args, **kwargs):
        raise NoResultFound("No result found")

    def __enter__(self): return self
    def __exit__(self ,exc_type, exc_val, exc_tb): pass

def test_get_person():
    mock_connection = MockConnection()
    repo = PeopleRepository(mock_connection)
    repo.get_person(3)

    mock_connection.session.query.assert_called_once_with(PeopleTable)
    mock_connection.session.filter.assert_called_once_with(PeopleTable.id == 3)

def test_insert_person():
    first_name = "Felipe"
    last_name = "Viana"
    age = 30
    pet_id = 2

    mock_connection = MockConnection()
    repo = PeopleRepository(mock_connection)
    repo.insert_person(
        first_name=first_name,
        last_name=last_name,
        age=age,
        pet_id=pet_id
    )

    mock_connection.session.add.assert_called()
    called_person = mock_connection.session.add.call_args[0][0]
    assert isinstance(called_person, PeopleTable)
    assert called_person.first_name == "Felipe"

def test_list_person_no_result():
    mock_connection = MockConnectionNoResult()
    repo = PeopleRepository(mock_connection)
    response = repo.get_person(1)

    mock_connection.session.query.assert_called_once_with(PeopleTable)
    mock_connection.session.filter.assert_not_called()

    assert response is None

def test_insert_person_error():
    first_name = "Felipe"
    last_name = "Viana"
    age = 30
    pet_id = 19

    mock_connection = MockConnectionNoResult()
    repo = PeopleRepository(mock_connection)

    with pytest.raises(Exception, match="No result found"):
        repo.insert_person(
                first_name=first_name,
                last_name=last_name,
                age=age,
                pet_id=pet_id
        )

    mock_connection.session.add.assert_called()
    mock_connection.session.rollback.assert_called()
