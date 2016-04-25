# -*- coding: utf-8 -*-
import requests

from pydeform.auth import (
    get_session_http_auth_header,
    get_token_http_auth_header
)
from pydeform.resources import (
    CollectionListResource,
    CollectionOneResource,
    CurrentProjectInfoResource,
    DocumentListResource,
    DocumentOneResource,
    NonAuthUserResource,
    ProjectListResource,
    ProjectOneResource,
    SessionUserResource
)
from pydeform.utils import get_base_uri

_DOCS_DATA = {
    'requests_session_url': (
     'http://docs.python-requests.org/en/master/user/advanced/#session-objects'
    ),
    'requests_request_url': (
     'http://docs.python-requests.org/en/master/api/#requests.request'
    )
}


class Client(object):
    __doc__ = """Deform.io python client class.

    Parameters:

    * `host` - HTTP server host. E.g. `deform.io`.
    * `port` - HTTP server port. Default is `None`.
    * `secure` - if `True` client will make secure request via `https`.
       Default is `True`.
    * `requests_session` - python requests' [Session][requests-session]
       instance. Default is `None`.
    * `request_defaults` - python requests' [request][requests-request]
       defaults. Default is `None`.
    * `api_base_path` - HTTP server's api uri base path. Default is `/api/`.

    Example:

    ```python
    client = Client(host='deform.io')
    ```

    [requests-session]: %(requests_session_url)s
    [requests-request]: %(requests_request_url)s

    """ % {
        'requests_session_url': _DOCS_DATA['requests_session_url'],
        'requests_request_url': _DOCS_DATA['requests_request_url'],
    }

    def __init__(self,
                 host,
                 port=None,
                 secure=True,
                 requests_session=None,
                 request_defaults=None,
                 api_base_path='/api/'):
        self.host = host
        self.port = port
        self.secure = secure
        self.requests_session = requests_session or requests.Session()
        self.request_defaults = request_defaults
        self.api_base_path = api_base_path
        self.user = NonAuthUserResource(
            base_uri=get_base_uri(
                host=self.host,
                port=self.port,
                secure=self.secure,
                api_base_path=self.api_base_path
            ),
            auth_header=None,
            requests_session=self.requests_session,
            request_defaults=self.request_defaults
        )

    def auth(self, auth_type, auth_key, project_id=None):
        """Creates authenticated client.

        Parameters:

        * `auth_type` - Authentication type. Use `session` for auth
          by session key. Use `token` for auth by token.
        * `auth_key` - Authentication `session key` or `token`.
        * `project_id` - Project identifier. Must be provided for
          `token` authentication. Default is `None`.

        Returns:

        * Instance of [SessionAuthClient](#sessionauthclient) if
          `auth_type` is `session`.
        * Instance of [ProjectClient](#projectclient) if
          `auth_type` is `token`

        Raises:

        * ValueError: if `project_id` parameter was not provided

        Examples:

        For auth with `session` you should obtain session key by
        [Client.user.login](#clientuserlogin) providing
        your account's email and password:

        ```python
        client = Client(host='deform.io')
        session_client = client.auth(
            'session',
            client.user.login(
                email='email@example.com',
                password='password'
            ),
        )
        print session_client
        <pydeform.client.SessionAuthClient object at 0x10c585650>
        ```

        Authentication with `token` example:

        ```python
        client = Client(host='deform.io')
        session_client = client.auth(
          'token',
          auth_key='token-value',
          project_id='some-project',
        )
        print session_client
        <pydeform.client.ProjectClient object at 0x11c585650>
        ```

        """
        if auth_type == 'session':
            return SessionAuthClient(
                auth_header=get_session_http_auth_header(auth_key),
                host=self.host,
                port=self.port,
                secure=self.secure,
                requests_session=self.requests_session,
                request_defaults=self.request_defaults,
                api_base_path=self.api_base_path,
            )
        elif auth_type == 'token':
            if not project_id:
                msg = 'You should provide project_id for token authentication'
                raise ValueError(msg)
            return ProjectClient(
                base_uri=get_base_uri(
                    project=project_id,
                    host=self.host,
                    port=self.port,
                    secure=self.secure,
                    api_base_path=self.api_base_path
                ),
                auth_header=get_token_http_auth_header(auth_key),
                requests_session=self.requests_session,
                request_defaults=self.request_defaults,
            )


class SessionAuthClient(object):
    """Session auth client.

    You should not initalize this client manually.
    Use [Client.auth](#clientauth) method with ``session`` authentication.
    """

    def __init__(self,
                 auth_header,
                 host,
                 port,
                 secure,
                 requests_session,
                 request_defaults,
                 api_base_path):
        self.host = host
        self.port = port
        self.secure = secure
        self.requests_session = requests_session
        self.request_defaults = request_defaults
        self.auth_header = auth_header
        self.api_base_path = api_base_path
        self.base_uri = get_base_uri(
            host=self.host,
            port=self.port,
            secure=self.secure,
            api_base_path=self.api_base_path
        )
        resource_kwargs = {
            'base_uri': self.base_uri,
            'auth_header': auth_header,
            'requests_session': requests_session,
            'request_defaults': request_defaults
        }
        self.user = SessionUserResource(**resource_kwargs)
        self.projects = ProjectListResource(**resource_kwargs)
        self.project = ProjectOneResource(**resource_kwargs)

    def use_project(self, project_id):
        """Creates an instance of [ProjectClient](#projectclient),
        providing session authentication.

        Parameters:

        * `project_id` - project identifier.

        Returns:

        Instance of [ProjectClient](#projectclient) with
        session authentication.

        Example:

        ```python
        client = Client('deform.io')
        session_client = client.auth(
            'session',
            client.user.login('email@example.com', 'password')
        )
        session_client.use_project('some-project-id')
        ```

        """
        return ProjectClient(
            base_uri=get_base_uri(
                project=project_id,
                host=self.host,
                port=self.port,
                secure=self.secure,
                api_base_path=self.api_base_path
            ),
            auth_header=self.auth_header,
            requests_session=self.requests_session,
            request_defaults=self.request_defaults,
        )


class ProjectClient(object):
    """Project client.

    You should not initalize this client manually.
    Use [Client.auth](#clientauth) method with ``token`` authentication or
    [SessionAuthClient.use_project](#sessionauthclientuse_project) method.
    """

    def __init__(self,
                 base_uri,
                 auth_header,
                 requests_session,
                 request_defaults):
        resource_kwargs = {
            'base_uri': base_uri,
            'auth_header': auth_header,
            'requests_session': requests_session,
            'request_defaults': request_defaults
        }
        self.base_uri = base_uri
        self.auth_header = auth_header
        self.request_session = requests_session
        self.request_defaults = request_defaults
        self.info = CurrentProjectInfoResource(**resource_kwargs)
        self.collections = CollectionListResource(**resource_kwargs)
        self.collection = CollectionOneResource(**resource_kwargs)
        self.documents = DocumentListResource(**resource_kwargs)
        self.document = DocumentOneResource(**resource_kwargs)
