# -*- coding: utf-8 -*-
from requests.exceptions import ConnectionError as RequestsConnectionError
from requests.exceptions import ConnectTimeout as RequestsConnectTimeout
from requests.exceptions import ReadTimeout as RequestsReadTimeout


class DeformException(Exception):
    """Base Deform.io exception.

    Could be used for catching all Deform.io specific exception.

    ```python
    try:
        deform_client.collections.find()
    except DeformException as e:
        print 'Deform.io specific exception raised'
    ```
    """
    message = 'Deform error'


class HTTPError(DeformException):
    """Base exception for errors produced at the HTTP layer.

    These types of exceptions containes additional parameters:

    * `requests_error` - original [requests exception][requests-exception].
    * `errors` - list of errors.

    [requests-exception]: http://docs.python-requests.org/en/master/api/#exceptions
    """  # noqa
    message = 'HTTP error'
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
        error = self.message
        if self.errors:
            error = '%s:\n%s' % (
                error,
                '\n'.join([
                    '* "%s" - %s' % (i['property'], i['message'])
                    for i in self.errors
                ])
            )
        return error


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
    [ConnectTimeout](#connecttimeout) and
    [ReadTimeout](#readtimeout) errors.
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
