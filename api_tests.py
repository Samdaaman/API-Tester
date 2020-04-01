from api_test import API_Test
from typing import List, Tuple, Optional
import backdoor_interface as b
import api_interface as a
import reponses as r
import json
from exceptions import BePatientException


def set_base_url(base_url: str):
    a.base_url = base_url
    b.base_url = base_url


def get_tests_from_json(json_tests: dict) -> List[API_Test]:
    list_tests = []
    for json_test in json_tests:
        name = 'unknown name'
        try:
            name = json_test['name']
            description = json_test['description']
            if 'reload_before' in json_test:
                reload_before = json_test['reload_before']
            else:
                reload_before = True

            list_steps: List[Tuple[a.Request, Optional[r.Response]]] = []
            for json_step in json_test['steps']:  # type: dict
                method = json_step['method']
                url = json_step['url']

                if method == 'GET':
                    request = a.Get(url)
                else:
                    raise BePatientException



                if 'response' in json_step:
                    response = json_step['response']
                else:
                    response = None

                list_steps.append((request, response))
            list_tests.append(API_Test(name, description, tuple(list_steps), reload_before))

        except BePatientException:
            print(f'The test {name} has steps which aren\'t implemented yet')
        except KeyError as e:
            print(f'The key: "{e.args[0]}" was not found in test: "{name}"')

    return list_tests


with open('api_tests.json', 'r') as fh:
    json_data = json.loads(fh.read())

basic_tests: List[API_Test] = get_tests_from_json(json_data["basic_tests"])
users_tests: List[API_Test] = get_tests_from_json(json_data["users_tests"])
petitions_tests: List[API_Test] = get_tests_from_json(json_data["petitions_tests"])
signatures_tests: List[API_Test] = get_tests_from_json(json_data["signatures_tests"])
categories_tests: List[API_Test] = get_tests_from_json(json_data["categories_tests"])


# Basic Tests
# basic_tests.append(API_Test('Test site connection', 'GET to the root url (is the site up)', ((a.Get('/../../'), None),), False))


# User Tests
# users_tests.append(API_Test('User GET (unauthed)', '', ((a.Get('/users/1'), r.Response(200, {'name': 'Eleanor Shellstrop', 'city': 'Phoenix', 'country': 'USA'})),)))


# All Tests
all_tests = basic_tests + users_tests + petitions_tests + signatures_tests + categories_tests
