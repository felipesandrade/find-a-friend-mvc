from typing import List # python 3.8
from sqlalchemy.orm.exc import NoResultFound
from src.models.sqlite.entities.pets import PetsTable

class PetsRepository:
    def __init__(self, db_connection) -> None:
        self.__db_connection = db_connection

    def list_pets(self) -> List[PetsTable]:
        with self.__db_connection as database:
            try:
                pets = database.session.query(PetsTable).all()
                return pets
            except NoResultFound:
                return []

    def delete_pets(self, name: str) -> int:
        with self.__db_connection as database:
            try:
                result = ( database.session
                                .query(PetsTable)
                                .filter(PetsTable.name == name)
                                .delete()
                         )
                database.session.commit()
                return result
            except Exception as exception:
                database.session.rollback()
                raise exception
            