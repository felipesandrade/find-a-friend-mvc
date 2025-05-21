from unittest import mock
import pytest
from mock_alchemy.mocking import UnifiedAlchemyMagicMock
from sqlalchemy.orm.exc import NoResultFound
from src.models.sqlite.entities.pets import PetsTable
from .pets_repository import PetsRepository

class MockConnection: # Simula o acesso ao banco de dados e retorna um resultado
    def __init__(self) -> None:
        self.session = UnifiedAlchemyMagicMock(
            data=[
                (
                    [mock.call.query(PetsTable)], # query
                    [
                        PetsTable(name="dog", type="dog"),
                        PetsTable(name="cat", type="cat")
                    ] # resultado
                )
            ]
        )

    def __enter__(self): return self
    def __exit__(self, exc_type, exc_val, exc_tb): pass
class MockConnectionNoResult: # Simula erro
    def __init__(self) -> None:
        self.session = UnifiedAlchemyMagicMock()
        self.session.query.side_effect = self.__raise_no_result_found

    def __raise_no_result_found(self, *args, **kwargs):
        raise NoResultFound("No result found")

    def __enter__(self): return self
    def __exit__(self, exc_type, exc_val, exc_tb): pass

def test_list_pets(): # Testando retorno da lista de pets
    mock_connection = MockConnection()
    repo = PetsRepository(mock_connection)
    response = repo.list_pets()

    # verifica se a query foi chamada 1 vez com o PetsTable
    mock_connection.session.query.assert_called_once_with(PetsTable)
    # verifica se o all foi chamado
    mock_connection.session.all.assert_called_once()
    # verifica se o filtro foi chamado
    mock_connection.session.filter.assert_not_called()
    assert response[0].name == "dog"

def test_delete_pet(): # Testando deleção de pet
    mock_connection = MockConnection()
    repo = PetsRepository(mock_connection)

    repo.delete_pets("petName")

    mock_connection.session.query.assert_called_once_with(PetsTable)
    # verifica se o filtro foi chamado
    mock_connection.session.filter.assert_called_once_with(PetsTable.name == "petName")
    # verifica se o delete foi chamado
    mock_connection.session.delete.assert_called_once()

def test_list_pets_no_result(): # Testando retorno da lista de pets
    mock_connection = MockConnectionNoResult()
    repo = PetsRepository(mock_connection)
    response = repo.list_pets()

    # verifica se a query foi chamada 1 vez com o PetsTable
    mock_connection.session.query.assert_called_once_with(PetsTable)
    # verifica se o all foi chamado
    mock_connection.session.all.assert_not_called()
    # verifica se o filtro foi chamado
    mock_connection.session.filter.assert_not_called()

    assert response == []

def test_delete_pet_error(): # Testando deleção de pet
    mock_connection = MockConnectionNoResult()
    repo = PetsRepository(mock_connection)

    with pytest.raises(Exception):
        repo.delete_pets("petName")

    mock_connection.session.rollback.assert_called_once()
