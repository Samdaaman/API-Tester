import requests as req
from exceptions import BaseURLNotSetException, BePatientException, NotAllowedException

base_url = None


def url(rel_url: str):
    _check_base_url()
    return base_url + rel_url


def _check_base_url():
    if base_url is None:
        raise BaseURLNotSetException()


def backdoor_reload():
    _check_base_url()
    req.post(url('/reload'))


class Request:
    def __init__(self, rel_url: str, auth: bool = False):
        self.rel_url = rel_url
        self.auth = auth

    def send(self) -> req.Response:
        raise NotAllowedException


class Get(Request):
    def send(self) -> req.Response:
        if self.auth:
            raise BePatientException
        else:
            return req.get(url(self.rel_url))
