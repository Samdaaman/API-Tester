from exceptions import BePatientException, CouldNotConnectToSiteException
from typing import Tuple, Optional
from api_interface import Request, backdoor_reload
from reponses import Response as Expected_response
from requests.exceptions import ConnectionError


class API_Test:
    def __init__(self, name: str, description: str, method: Tuple[Tuple[Request, Optional[Expected_response]]], reload_before: bool = True):
        self.name = name
        self.description = description
        self.method = method
        self.failure_reason: str = ''
        self.reload_before = reload_before

    def run_test(self):
        if self.method is None:
            raise BePatientException
        try:
            if self.reload_before:
                backdoor_reload()
            for request, expected_response in self.method:  # type: Request, Expected_response
                actual_response = request.send()
                if expected_response is not None:
                    expected_response.check(actual_response)
        except ConnectionError:
            raise CouldNotConnectToSiteException()

    def __str__(self):
        return f'{self.name}'
