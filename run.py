from api_tester import API_Tester
import api_tests

# Settings
api_tests.set_base_url_baseline('http://csse-s365.canterbury.ac.nz:4001/api/v1')  # url of baseline server
# api_tests.set_base_url_test('http://127.0.0.1:4200/api/v1')  # url of server to test against the baseline
api_tests.set_base_url_test('http://csse-s365.canterbury.ac.nz:4120/api/v1')
continue_on_failure = True
log_success = True

# Getting Tests
api_tests_to_run = api_tests.all_tests

# Initialising tester and running tests
api_tester = API_Tester(continue_on_failure, log_success)
api_tester.run_tests(api_tests_to_run)
