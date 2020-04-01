from typing import List
from api_test import API_Test
from exceptions import FailureException, FatalException
from api_interface import initial_test


class API_Tester:
    def __init__(self, continue_on_failure: bool, log_success: bool):
        self.log_success = log_success
        self.continue_on_failure = continue_on_failure

    def run_tests(self, api_tests: List[API_Test]):
        try:
            if not isinstance(api_tests, list):
                raise FatalException('api_tests parameter must be a list of api_tests')

            initial_test(silent=True)
            print('----------------------------------------')
            print(f'Running {len(api_tests)} tests')
            print('----------------------------------------')

            success_count = 0
            for api_test in api_tests:  # type: API_Test
                try:
                    api_test.run_test()

                except FailureException as e:
                    print(f'Test failed {api_test}{" - " + api_test.description if api_test.description != "" else ""} - {e}\n')

                else:
                    if self.log_success:
                        print(f'Test passed {api_test}\n')
                    success_count += 1

        except FatalException as e:
            print('----------------------------------------')
            print(e)

        except KeyboardInterrupt:
            print('----------------------------------------')
            print('Stopped')

        except Exception as e:
            print('----------------------------------------')
            print(f'Unhandled and Unknown exception\n{e.__class__}\n{e.args}')
            raise e

        else:
            print('----------------------------------------')
            print(f'Done, passed {success_count}/{len(api_tests)} tests successfully')