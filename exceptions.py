# Fatal exceptions
class FatalException(Exception):
    def __init__(self, *args):
        if self.args:
            self.message = args[0]
        else:
            self.message = None

    def __str__(self):
        if self.message:
            return f'Fatal Exception: {self.message}'
        else:
            return 'Unknown Fatal Exception'


class NotAllowedException(FatalException):
    def __init__(self):
        self.message = 'You are not allowed to do this'


class BaseURLNotSetException(FatalException):
    def __init__(self):
        self.message = ' because the base url parameter was not set'


class FailureException(Exception):
    def __init__(self, *args):
        if self.args:
            self.message = args[0]
        else:
            self.message = None

    def __str__(self):
        if self.message:
            return f'Reason: {self.message}'
        else:
            return 'Reason: for an unknown reason'


# Failure exceptions are below (not fatal only fail the test)
class UnknownStatusCodeException(FailureException):
    def __init__(self, unknown_status_code: int):
        self.message = f'status code {unknown_status_code} is unknown'


class BePatientException(FailureException):
    def __init__(self):
        self.message = 'test is not implemented yet'


class StatusMessageMissMatchException(FailureException):
    def __init__(self, expected_message: str, got_message: str):
        self.message = f'expected status message {expected_message} got {got_message}'


class StatusCodeMissMatchException(FailureException):
    def __init__(self, expected_code: int, got_code: int):
        self.message = f'expected status code {expected_code} got {got_code}'


class ContentMissMatchException(FailureException):
    def __init__(self, expected_content=None, got_content=None):
        if expected_content is None or got_content is None:
            self.message = 'content not as expected'
        else:
            self.message = f'expected content {expected_content} got {got_content}'


class CouldNotConnectToSiteException(FailureException):
    def __init__(self):
        self.message = f'it appears a connection to the site could not be established'
