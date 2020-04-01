from typing import Union


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
    def __init__(self, *args):
        if args:
            self.message = f'You are not allowed to do this ({args[0]})'
        else:
            self.message = 'You are not allowed to do this (unknown)'


class BaseURLNotSetException(FatalException):
    def __init__(self):
        self.message = 'The base url parameter was not set'


class InitialTestFailureException(FatalException):
    def __init__(self, url):
        self.message = f'Initial connection to the site {url} could not be made'


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
    def __init__(self, *args):
        if self.args:
            self.message = f'{args[0]} is not implemented yet'
        else:
            self.message = 'This is not implemented yet'


class StatusMessageMissMatchException(FailureException):
    def __init__(self, url: str, expected_message: str, got_message: str, data='None'):
        self.message = f'Status Message mismatch for {url}, expected {expected_message} got {got_message}, data = {data}'


class StatusCodeMissMatchException(FailureException):
    def __init__(self, url: str, expected_code: Union[int, str], got_code: Union[str, int], data='None'):
        self.message = f'Status Code mismatch for {url}, expected {expected_code} got {got_code}, data = {data}'


class ContentMismatchException(FailureException):
    def __init__(self, url: str, mismatches=None, data='None'):
        if mismatches is None:
            self.message = f'Content Mismatch: content not as expected, data = {data}'
        else:
            bullet = '\n --- '
            self.message = f'Content Mismatch for {url}, data = {data}{bullet}{bullet.join(mismatches)}'


class CouldNotConnectToSiteException(FailureException):
    def __init__(self):
        self.message = f'it appears a connection to the site could not be established'
