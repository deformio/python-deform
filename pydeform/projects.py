# -*- coding: utf-8 -*-
from pydeform.collections import Collections
from pydeform.utils import get_base_uri, uri_join


class ProjectsIterator(object):
    def create(self, identity, name):
        pass


class Projects(object):
    def __init__(self,
                 host,
                 port,
                 secure,
                 api_base_path,
                 auth,
                 requests_session):
        self.host = host
        self.port = port
        self.secure = secure
        self.api_base_path = api_base_path
        self.auth = auth
        self.requests_session = requests_session

    def __call__(self, identity=None):
        if identity:
            return Project(
                base_uri=get_base_uri(
                    project=identity,
                    host=self.host,
                    port=self.port,
                    secure=self.secure,
                    api_base_path=api_base_path
                ),
                auth=self.auth,
                requests_session=self.requests_session
            )
        else:
            return ProjectsIterator()


class Project(object):
    def __init__(self, base_uri, auth, requests_session):
        self.base_uri = base_uri
        self.auth = auth
        self.requests_session = requests_session
        self.collections = Collections(
            base_uri=uri_join(base_uri, 'collections')
        )

    def get_data(self):
        self.requests_session.get(self.base_uri)
