# -*- coding: utf-8 -*-
import requests

from pydeform.auth import (
    get_session_id,
    get_session_http_auth_header,
    get_token_http_auth_header,
)
from pydeform.utils import (
    get_base_uri,
    uri_join,
)
from pydeform.resources import (
    CurrentProjectInfoResource,
    ProjectListResource,
    ProjectOneResource,
    UserOneResource,
    CollectionListResource,
    CollectionOneResource,
    DocumentListResource,
    DocumentOneResource,
)


class Client(object):
    def __init__(self,
                 host,
                 port=None,
                 secure=True,
                 requests_session=None,
                 api_base_path='/api/'):
        self.host = host
        self.port = port
        self.secure = secure
        self.requests_session = requests_session or requests.Session()
        self.api_base_path = api_base_path

    def login(self, email, password, timeout=None):
        return self.auth(
            'session',
            auth_key=get_session_id(
                base_uri=get_base_uri(
                    host=self.host,
                    port=self.port,
                    secure=self.secure,
                    api_base_path=self.api_base_path
                ),
                email=email,
                password=password,
                requests_session=self.requests_session,
                timeout=timeout
            )
        )

    def auth(self, auth_type, auth_key, project_id=None):
        # todo: test me

        if auth_type == 'session':
            auth_header = get_session_http_auth_header(auth_key)
            return SessionAuthClient(
                auth_header=auth_header,
                host=self.host,
                port=self.port,
                secure=self.secure,
                requests_session=self.requests_session,
                api_base_path=self.api_base_path,
            )
        elif auth_type == 'token':
            if not project_id:
                raise ValueError('You should provide project_id for token authentication')
            return ProjectClient(
                base_uri=get_base_uri(
                    project=project_id,
                    host=self.host,
                    port=self.port,
                    secure=self.secure,
                    api_base_path=self.api_base_path
                ),
                auth_header=get_token_http_auth_header(auth_key),
                requests_session=self.requests_session
            )

    def register(self, email, password, timeout=None):
        pass

    def confirm(self, code, timeout=None):
        pass


class SessionAuthClient(object):
    def __init__(self,
                 auth_header,
                 host,
                 port,
                 secure,
                 requests_session,
                 api_base_path):
        self.host = host
        self.port = port
        self.secure = secure
        self.requests_session = requests_session
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
            'requests_session': requests_session
        }
        self.user = UserOneResource(**resource_kwargs)
        self.projects = ProjectListResource(**resource_kwargs)
        self.project = ProjectOneResource(**resource_kwargs)

    def use_project(self, project_id):
        return ProjectClient(
            base_uri=get_base_uri(
                project=project_id,
                host=self.host,
                port=self.port,
                secure=self.secure,
                api_base_path=self.api_base_path
            ),
            auth_header=self.auth_header,
            requests_session=self.requests_session
        )


class ProjectClient(object):
    def __init__(self,
                 base_uri,
                 auth_header,
                 requests_session):
        resource_kwargs = {
            'base_uri': base_uri,
            'auth_header': auth_header,
            'requests_session': requests_session
        }
        self.auth_header = auth_header
        self.info = CurrentProjectInfoResource(**resource_kwargs)
        self.collections = CollectionListResource(**resource_kwargs)
        self.collection = CollectionOneResource(**resource_kwargs)
        self.documents = DocumentListResource(**resource_kwargs)
        self.document = DocumentOneResource(**resource_kwargs)
