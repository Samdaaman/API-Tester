from exceptions import BePatientException, CouldNotConnectToSiteException, FailureException
from typing import Tuple, Optional, Union
from api_interface import Request, backdoor_reload, set_auth_tokens
from requests.exceptions import ConnectionError


def _run_custom_test(test_name: str):
    custom_tests = {
        'user-login': _custom_user_login,
        'user-register-then-login': _custom_user_register_then_login
    }
    if test_name in custom_tests:
        try:
            custom_tests[test_name]()
        except FailureException:
            raise
        except Exception as e:
            raise FailureException(f'Error while running custom test {test_name}, {e.__class__}, {e}, {e.args}')
    else:
        raise BePatientException(f'Custom test {test_name}')


def _custom_user_login():
    data = {'email': 'e.shellstrop@hotmail.com', 'password': 'legitsnack'}
    token_test = Request('/users/login', 'POST', 0, data).send(False, 200).json()['token']
    token_database = Request('/executeSql', 'POST', 0, 'SELECT auth_token FROM User WHERE user_id = 1;').send(False, 200).json()[0]['auth_token']
    if token_test != token_database:
        raise FailureException('Custom user login test failed, token does not match')


def _custom_user_register_then_login():
    data = {'name': 'test_user', 'email': 'new_user@yeet.com', 'password': 'please'}
    Request('/users/register', 'POST', 0, data).send(False, 201)
    token_test = Request('/users/login', 'POST', 0, data).send(False, 200).json()['token']
    token_database = Request('/executeSql', 'POST', 0, 'SELECT auth_token FROM User WHERE user_id = 11;').send(False, 200).json()[0]['auth_token']
    if token_test != token_database:
        raise FailureException('Custom user login test failed, token does not match')


class API_Test:
    def __init__(self, name: str, description: str, auth: bool, steps: Union[Tuple[Request], str]):
        self.name = name
        self.description = description
        self.auth = auth
        self.steps = steps

    def run_test(self):
        if self.steps is None:
            raise BePatientException(f'Test {self.name}')

        try:
            backdoor_reload(both=True)
            if self.auth:
                set_auth_tokens()
            if isinstance(self.steps, str):
                _run_custom_test(self.steps)
            else:
                for request in self.steps:  # type: Request
                    request.send_and_check(use_auth=self.auth)

        except ConnectionError:
            raise CouldNotConnectToSiteException()

    def __str__(self):
        return f'{self.name}'
