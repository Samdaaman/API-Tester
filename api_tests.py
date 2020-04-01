from api_test import API_Test
from typing import List
import backdoor_interface as b
import api_interface as a
import reponses as r


def set_base_url(base_url: str):
    a.base_url = base_url
    b.base_url = base_url


basic_tests: List[API_Test] = []
users_tests: List[API_Test] = []
petitions_tests: List[API_Test] = []
signatures_tests: List[API_Test] = []
categories_tests: List[API_Test] = []

# Basic Tests
basic_tests.append(API_Test('Test site connection', 'GET to the root url (is the site up)', ((a.Get('/../../'), None),), False))


# User Tests
users_tests.append(API_Test('User GET (unauthed)', '', ((a.Get('/users/1'), r.Response(200, {'name': 'Eleanor Shellstrop', 'city': 'Phoenix', 'country': 'USA'})),)))


# All Tests
all_tests = basic_tests + users_tests + petitions_tests + signatures_tests + categories_tests
