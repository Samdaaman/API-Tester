from api_test import API_Test
from typing import List, Tuple, Optional, Union
import api_interface as a
import json
from exceptions import BePatientException, NotAllowedException


def set_base_url_baseline(base_url_baseline: str):
    a.base_url_baseline = base_url_baseline


def set_base_url_test(base_url_test: str):
    a.base_url_test = base_url_test


def get_tests_from_json(json_tests: dict) -> List[API_Test]:
    list_tests = []
    for json_test in json_tests:  # type: dict
        name = 'unknown name'
        try:
            name = json_test['name']
            description = json_test.get('description', '')
            auth = json_test.get('auth', False)
            list_order_matters = json_test.get('array_order_matters', True)

            list_steps: List[a.Request] = []

            steps = json_test['steps']
            if isinstance(steps, list):
                for json_step in steps:  # type: Union[str, dict]
                    method = json_step['method']
                    url = json_step['url']
                    code = json_step['code']
                    data = json_step.get('data')
                    list_steps.append(a.Request(url, method, code, data, list_order_matters))

                list_tests.append(API_Test(name, description, auth, tuple(list_steps)))

            elif isinstance(steps, str):
                list_tests.append(API_Test(name, description, auth, steps))

            else:
                NotAllowedException(f'Unknown type of steps: {type(steps)}')

        except BePatientException:
            print(f'The test {name} has steps which aren\'t implemented yet')
        except KeyError as e:
            print(f'The key: "{e.args[0]}" was not found in test: "{name}"')

    return list_tests


with open('api_tests.json', 'r') as fh:
    json_data = json.loads(fh.read())

users_tests: List[API_Test] = get_tests_from_json(json_data.get("users_tests"))
petitions_tests: List[API_Test] = get_tests_from_json(json_data.get("petitions_tests"))
signatures_tests: List[API_Test] = get_tests_from_json(json_data.get("signatures_tests"))
categories_tests: List[API_Test] = get_tests_from_json(json_data.get("categories_tests"))


# All Tests
all_tests = users_tests + petitions_tests + signatures_tests + categories_tests
