from typing import Union, List, Tuple
from api_test import API_Test
from exceptions import FailureException, FatalException


class API_Tester:
    def __init__(self, continue_on_failure: bool, max_failures: int, log_success: bool):
        self.log_success = log_success
        self.continue_on_failure = continue_on_failure
        self.max_failures = max_failures

    def run_tests(self, api_tests: List[API_Test]):
        try:
            if not isinstance(api_tests, list):
                raise FatalException('api_tests parameter must be a list of api_tests')

            for api_test in api_tests:  # type: API_Test
                if self.evaluate_test(api_test):
                    if self.log_success:
                        print(f'Test passed {api_test}')
                else:
                    print(f'Test failed {api_test}{" - " + api_test.description if api_test.description != "" else ""} - {api_test.failure_reason}')

        except FatalException as e:
            print(e)
            exit(1)
        except Exception as e:
            print(f'Unhandled and Unknown exception\n{e.__class__}\n{e.args}')
            raise e

    def evaluate_test(self, api_test: API_Test, failure_count: int = 0):
        try:
            api_test.run_test()

        except FailureException as e:
            api_test.failure_reason = str(e)
            return False

        except FatalException as e:
            raise e

        except Exception as e:
            print(f'Unknown exception #{failure_count+1}when running test {api_test} - {e.__class__} - {e.args} - continuing')
            if failure_count >= self.max_failures:
                raise e
            else:
                return self.evaluate_test(api_test, failure_count + 1)

        # If no exceptions occur the test was successful
        return True
