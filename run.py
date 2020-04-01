from api_tester import API_Tester
import api_tests

# Settings
api_tests.set_base_url('http://127.0.0.1:4200/api/v1')
# api_tests.set_base_url('http://csse-s365.canterbury.ac.nz:4001/api/v1')
continue_on_failure = True
max_failures = 1
log_success = True

# Getting Tests
api_tests_to_run = api_tests.all_tests

# Initialising tester and running tests
api_tester = API_Tester(continue_on_failure, max_failures, log_success)
print(f'Running {len(api_tests_to_run)} tests')
api_tester.run_tests(api_tests_to_run)
