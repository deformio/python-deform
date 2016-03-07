# -*- coding: utf-8 -*-
from requests.exceptions import (
    ConnectionError as RequestsConnectionError,
    ConnectTimeout as RequestsConnectTimeout,
    ReadTimeout as RequestsReadTimeout,
)


class DeformException(Exception):
    """Base Deform.io exception"""
    pass


class HTTPError(DeformException):
    """Errors produced at the HTTP layer."""

    def __init__(self, requests_error):
        # todo: test me
        self.requests_error = requests_error
        if self.requests_error.response is None:
            self.error = None
        else:
            self.error = self.requests_error.response.json().get('error')

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        if self.error:
            return '; '.join([i['message'] for i in self.error])
        else:
            name = type(self).__name__
            message = name[0]
            for i in name[1:]:
                if i.istitle():
                    message += ' '
                message += i.lower()
            return message


class AuthError(HTTPError):
    """Errors due to invalid authentication credentials."""
    pass


class ForbiddenError(HTTPError):
    pass


class NotFoundError(HTTPError):
    pass


class ValidationError(HTTPError):
    pass


class ConnectionError(HTTPError):
    """A Connection error occurred."""


class Timeout(HTTPError):
    """The request timed out.
    Catching this error will catch both
    :exc:`~pydeform.exceptions.ConnectTimeout` and
    :exc:`~pydeform.exceptions.ReadTimeout` errors.
    """


class ConnectTimeout(ConnectionError, Timeout):
    """The request timed out while trying to connect to the remote server.
    Requests that produced this error are safe to retry.
    """


class ReadTimeout(Timeout):
    """The server did not send any data in the allotted amount of time."""


STATUS_CODE_ERROR_MAP = {
    401: AuthError,
    403: ForbiddenError, # todo: test me
    404: NotFoundError, # todo: test me
    422: ValidationError  # todo: test me
}

REQUESTS_ERROR_MAP = {
    RequestsConnectionError: ConnectionError,
    RequestsConnectTimeout: ConnectTimeout, # todo: test me
    RequestsReadTimeout: ReadTimeout,
}
