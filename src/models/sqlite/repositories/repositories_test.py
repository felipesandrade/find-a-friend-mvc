import pytest
from src.models.sqlite.settings.connection import db_connection_handler
from .pets_repository import PetsRepository
from .people_repository import PeopleRepository

db_connection_handler.connection_to_db()

@pytest.mark.skip(reason="interacao com o banco")
def test_list_pets():
    repo = PetsRepository(db_connection_handler)
    response = repo.list_pets()
    print()
    print(response)

@pytest.mark.skip(reason="interacao com o banco")
def test_delete_pet():
    name = "belinha"

    repo = PetsRepository(db_connection_handler)
    result = repo.delete_pets(name)
    assert result == 1

@pytest.mark.skip(reason="interacao com o banco")
def test_insert_person():
    first_name = "Felipe"
    last_name = "Viana de Andrade"
    age = 40
    pet_id = 1

    repo = PeopleRepository(db_connection_handler)
    repo.insert_person(first_name, last_name, age, pet_id)

@pytest.mark.skip(reason="interacao com o banco")
def test_get_person():
    person_id = 1

    repo = PeopleRepository(db_connection_handler)
    response = repo.get_person(person_id)
    print()
    print(response)
    print(response.pet_name)
