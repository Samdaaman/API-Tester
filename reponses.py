from requests import Response as requests_Response
from typing import Union
from exceptions import (
                        UnknownStatusCodeException,
                        BePatientException,
                        StatusCodeMissMatchException,
                        StatusMessageMissMatchException,
                        ContentMissMatchException
                        )

class Response:
    def __init__(self, code: int, content: Union[dict, str, None] = None, json: bool = True):
        self.code = code
        self.content = content
        self.json = json

    def check(self, actual_response: requests_Response):
        check_response(actual_response, self)


def _lookup_code(code: int):
    codes_dict = {200: 'OK', 201: 'Created'}
    if code in codes_dict:
        return codes_dict[code]
    else:
        raise UnknownStatusCodeException(code)


def _compare_dicts(dict1: dict, dict2: dict) -> bool:
    if not (isinstance(dict1, dict) and isinstance(dict2, dict)):
        return False

    if len(dict1.keys()) != len(dict2.keys()):
        return False

    for key1 in dict1:
        if key1 in dict2:
            if dict2[key1] != dict1[key1]:
                return False
    return True


def _check_content(response: requests_Response, content: Union[dict, str, None], json):
    if content is None:
        return True
    if json:
        if not _compare_dicts(response.json(), content):
            raise ContentMissMatchException(content, response.json())
    else:
        if isinstance(content, str):
            content = content.encode('utf-8')
        else:
            raise ContentMissMatchException('unknown expected content type', '')
        if not response.content == content:
            raise ContentMissMatchException(str(content), str(response.content))


def check_response(actual_response: requests_Response, expected_response: Response):
    if expected_response.code == actual_response.status_code:
        if _lookup_code(expected_response.code) == actual_response.reason:
            return _check_content(actual_response, expected_response.content, expected_response.json)
        else:
            raise StatusMessageMissMatchException(_lookup_code(expected_response.code), actual_response.reason)
    raise StatusCodeMissMatchException(expected_response.code, actual_response.status_code)
