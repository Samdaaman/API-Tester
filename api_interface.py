from requests import Response, get, post, delete, put, patch
from typing import Union, Optional
from exceptions import (BaseURLNotSetException,
                        InitialTestFailureException,
                        UnknownStatusCodeException,
                        BePatientException,
                        StatusCodeMissMatchException,
                        StatusMessageMissMatchException,
                        ContentMismatchException,
                        NotAllowedException
                        )
from json import JSONDecodeError

base_url_test = None
base_url_baseline = None

AUTH_TOKEN = 'i-swear-this-is-a-correct-token'


def _check_base_urls():
    if base_url_test is None or base_url_baseline is None:
        raise BaseURLNotSetException()


def initial_test(silent=False):
    if base_url_test is None or base_url_baseline is None:
        raise BaseURLNotSetException()
    _test_url(base_url_baseline)
    0 if silent else print('Can reach base url of baseline server')
    _test_url(base_url_test)
    0 if silent else print('Can reach base url of test server')


def _test_url(url):
    try:
        get(url)
    except:
        raise InitialTestFailureException(url)


def backdoor_reload(baseline: bool = None, both: bool = False):
    _check_base_urls()
    if both:
        Request('/reload', 'POST', 0, None).send(True, expected_code=201)
        Request('/reload', 'POST', 0, None).send(False, expected_code=201)
    elif baseline is not None:
        Request('/reload', 'POST', 0, None).send(baseline, expected_code=201)
    else:
        raise NotAllowedException('Reloading with incorrect parameters')


def set_auth_tokens():
    q = f'UPDATE User SET auth_token = \'{AUTH_TOKEN}\' WHERE user_id = 1;'
    Request('/executeSql', 'POST', 0, q).send(True, expected_code=200)
    Request('/executeSql', 'POST', 0, q).send(False, expected_code=200)


def _compare_lists(list1: list, list2: list, list_order_matters: bool, errors: list):
    if len(list1) != len(list2):
        errors.append(f'Expected arrays to have the same size:\n{list1}\n{list2}')

    if list_order_matters:
        for i in range(len(list1)):
            _compare_json_content(list1[i], list2[i], list_order_matters, errors)
    else:
        for item2 in list2:
            test_errors = []
            for item1 in list1:
                test_errors = []
                _compare_json_content(item1, item2, list_order_matters, test_errors)
                if len(test_errors) == 0:
                    break
            if len(test_errors) != 0:
                errors.append(f'{item2} not found in {list1}')


def _compare_dicts(dict1: dict, dict2: dict, list_order_matters: bool, errors: list):
    for key2 in dict2:
        if key2 not in dict1:
            errors.append(f'Key: {key2} is extra and not in {dict1}')

    for key1 in dict1:
        if key1 in dict2:
            _compare_json_content(dict1[key1], dict2[key1], list_order_matters, errors)
        else:
            errors.append(f'Key: {key1} missing from {dict2}')


def _compare_json_content(json1: Union[list, dict], json2: Union[list, dict], list_order_matters: bool, errors: list):
    if isinstance(json1, dict) and isinstance(json2, dict):
        _compare_dicts(json1, json2, list_order_matters, errors)
    elif isinstance(json1, list) and isinstance(json2, list):
        _compare_lists(json1, json2, list_order_matters, errors)
    elif isinstance(json1, (str, int)) and isinstance(json2, (int, str)):
        if json1 != json2:
            errors.append(f'Expected value "{json2}" to equal "{json1}"')


def _lookup_code(code: int):
    codes_dict = {200: 'OK', 201: 'Created', 400: 'Bad Request', 401: 'Unauthorized', 403: 'Forbidden', 404: 'Not Found', 500: 'Internal Server Error'}
    if code in codes_dict:
        return codes_dict[code]
    else:
        raise UnknownStatusCodeException(code)


def _merge_dicts(dict1: dict, dict2: dict):
    dict2.update(dict1)
    return dict2


class Request:
    def __init__(self, rel_url: str, method: str, code: int, data: Union[None, str, dict], list_order_matters: bool = False, auth: bool = False):
        self.rel_url = rel_url
        self.method = method
        self.code = code
        self.data = data
        self.list_order_matters = list_order_matters
        self.auth = auth
        self.response_baseline: Optional[Response] = None
        self.response_test: Optional[Response] = None

    def send_and_check(self, use_auth: bool = False) -> None:
        self.response_baseline = self.send(baseline=True, expected_code=self.code, use_auth=use_auth)
        self.response_test = self.send(baseline=False, expected_code=self.code, use_auth=use_auth)
        self._check_responses()

    def send(self, baseline: bool, expected_code: int, use_auth: bool = False) -> Response:
        url = (base_url_baseline if baseline else base_url_test) + self.rel_url
        auth_header = {} if not use_auth else {'X-Authorization': AUTH_TOKEN}

        response: Response
        if self.method == 'GET':
            response = get(url, headers=auth_header)

        elif self.method == 'POST':
            if isinstance(self.data, str):
                headers = _merge_dicts({'Content-Type': 'text/plain'}, auth_header)
                response = post(url, data=self.data, headers=headers)
            else:
                response = post(url, json=self.data, headers=auth_header)

        elif self.method == 'DELETE':
            response = delete(url, headers=auth_header)

        elif self.method == 'PATCH':
            response = patch(url, json=self.data, headers=auth_header)

        else:
            raise BePatientException(f'Method {self.method}')

        if expected_code is not None:
            if expected_code != response.status_code:
                raise StatusCodeMissMatchException(url, expected_code, response.status_code, self.data)

            if not response.reason.startswith(_lookup_code(expected_code)):
                raise StatusMessageMissMatchException(url, _lookup_code(expected_code), response.reason, self.data)

        return response

    def _check_responses(self):
        errors = []
        try:
            _compare_json_content(self.response_baseline.json(), self.response_test.json(), self.list_order_matters, errors)
        except JSONDecodeError:
            if self.response_baseline.content != self.response_test.content:
                errors.append('Raw content comparison error')
        if len(errors) > 0:
            errors.append(f'Expected: {self.response_baseline.json()}')
            errors.append(f'Got: {self.response_test.json()}')
            raise ContentMismatchException(self.rel_url, errors, self.data)
