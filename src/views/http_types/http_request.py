from typing import Dict  # python <= 3.8

class HttpRequest:
    def __init__(self, body: Dict = None, param: Dict = None) -> None:
        self.body = body
        self.param = param
