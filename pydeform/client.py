# -*- coding: utf-8 -*-
import requests

from pydeform.auth import (
    SessionAuth,
    TokenAuth,
)
from pydeform.projects import Projects, Project
from pydeform.paginators import PageNumberPaginator
from pydeform.utils import get_base_uri


class Client(object):
    def __init__(self,
                 host,
                 port=None,
                 secure=True,
                 project_id=None,
                 email=None,
                 password=None,
                 session_id=None,
                 token=None,
                 requests_session=None,
                 paginator_class=PageNumberPaginator,  # todo: limit_offset, cursor
                 api_base_path='/api/'):
        self.host = host
        self.port = port
        self.secure = secure
        self.requests_session = requests_session or requests.Session()
        if email and password:
            # self.projects = Projects(
            #     host=host,
            #     port=port,
            #     secure=secure,
            #     api_base_path=api_base_path,
            #     auth=SessionAuth(
            #         base_uri=get_base_uri(
            #             host=host,
            #             port=port,
            #             secure=secure,
            #             api_base_path=api_base_path
            #         )
            #         email=email,
            #         password=password,
            #         requests_session=self.requests_session,
            #     ),
            #     requests_session=self.requests_session,
            # )

        if session_id:


        elif project_id and token:
            # self.project = Project(
            #     base_uri=get_base_uri(
            #         project=project_id,
            #         host=host,
            #         port=port,
            #         secure=secure,
            #         api_base_path=api_base_path
            #     ),
            #     auth=TokenAuth(
            #         token=token,
            #     ),
            #     requests_session=self.requests_session,
            # )

    def register(self, email, password):
        pass

    def login(self, email, password):
        pass

    def confirm(self, code):
        pass
