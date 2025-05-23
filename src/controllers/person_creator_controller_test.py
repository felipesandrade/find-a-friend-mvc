import pytest
from .person_creator_controller import PersonCreatorController

class MockPeopleRepository:
    def insert_person(self, first_name: str, last_name: str, age: int, pet_id: int):
        pass

def test_create():
    person_info = {
        "first_name": "Fulano",
        "last_name": "deTal",
        "age": 30,
        "pet_id": 1
    }
    controller = PersonCreatorController(MockPeopleRepository())
    response = controller.create(person_info)

    assert response["data"]["type"] == "Person"
    assert response["data"]["count"] == 1
    assert response["data"]["attributes"] == person_info

def test_create_error():
    person_info = {
        "first_name": "Fulano123",
        "last_name": "deTal",
        "age": 30,
        "pet_id": 1
    }
    controller = PersonCreatorController(MockPeopleRepository())
    with pytest.raises(Exception):
        controller.create(person_info)
