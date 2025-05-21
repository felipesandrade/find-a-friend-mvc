from unittest import mock
from mock_alchemy.mocking import UnifiedAlchemyMagicMock
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

def test_list_pets(): # Testando retorno da lista de pets
    mock_connection = MockConnection()
    repo = PetsRepository(mock_connection)
    response = repo.list_pets()

    # verifica se a query foi chamada 1 vez com o PetsTable
    mock_connection.session.query.assert_called_once_with(PetsTable)
    mock_connection.session.all.assert_called_once() # verifica se o all foi chamado
    mock_connection.session.filter.assert_not_called() # verifica se o filtro foi chamado

    assert response[0].name == "dog"
