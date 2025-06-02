from src.controllers.interfaces.person_creator_controller import PersonCreatorControllerInterface
from .http_types.http_request import HttpRequest
from .http_types.http_response import HttpResponse
from .interfaces.view_interface import ViewInterface

class PersonCreatorView(ViewInterface):
    def __init__(self, person_creator_controller: PersonCreatorControllerInterface) -> None:
        self.__person_creator_controller = person_creator_controller

    def handle(self, http_request: HttpRequest) -> HttpResponse:
        person_info = http_request.body
        body_response = self.__person_creator_controller.create(person_info)

        return HttpResponse(status_code=201, body=body_response)
