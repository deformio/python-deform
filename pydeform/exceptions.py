# -*- coding: utf-8 -*-
from requests.exceptions import ConnectionError as RequestsConnectionError
from requests.exceptions import ConnectTimeout as RequestsConnectTimeout
from requests.exceptions import ReadTimeout as RequestsReadTimeout


class DeformException(Exception):
    """Base Deform.io exception"""
    message = 'Deform error'


class HTTPError(DeformException):
    """Errors produced at the HTTP layer."""
    message = 'Http error'
    errors = []

    def __init__(self, requests_error):
        # todo: test me
        self.requests_error = requests_error
        if self.requests_error.response is not None:
            message = self.requests_error.response.json().get(
                'result', {}
            ).get('message')
            if message:
                self.message = message
            errors = self.requests_error.response.json().get(
                'result', {}
            ).get('errors')
            if errors:
                self.errors = errors

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return self.message


class AuthError(HTTPError):
    """Errors due to invalid authentication credentials."""
    message = 'Auth error'


class ForbiddenError(HTTPError):
    message = 'Forbidden error'


class NotFoundError(HTTPError):
    message = 'Not found error'


class ValidationError(HTTPError):
    message = 'Validation error'


class ConflictError(HTTPError):
    message = 'Conflict error'


class ConnectionError(HTTPError):
    """A Connection error occurred."""
    message = 'Connection error'


class Timeout(HTTPError):
    """The request timed out.
    Catching this error will catch both
    :exc:`~pydeform.exceptions.ConnectTimeout` and
    :exc:`~pydeform.exceptions.ReadTimeout` errors.
    """
    message = 'Timeout'


class ConnectTimeout(ConnectionError, Timeout):
    """The request timed out while trying to connect to the remote server.
    Requests that produced this error are safe to retry.
    """
    message = 'Connect timeout'


class ReadTimeout(Timeout):
    """The server did not send any data in the allotted amount of time."""
    message = 'Read timeout'


STATUS_CODE_ERROR_MAP = {
    401: AuthError,  # todo: test me
    403: ForbiddenError,  # todo: test me
    404: NotFoundError,  # todo: test me
    409: ConflictError,  # todo: test me
    422: ValidationError,  # todo: test me
}

REQUESTS_ERROR_MAP = {
    RequestsConnectionError: ConnectionError,
    RequestsConnectTimeout: ConnectTimeout,  # todo: test me
    RequestsReadTimeout: ReadTimeout,
}
