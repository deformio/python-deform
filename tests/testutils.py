# -*- coding: utf-8 -*-
import unittest
import os
import json

import requests
from hamcrest import (
    assert_that,
    calling,
    raises
)

from pydeform import Client
from pydeform.utils import get_base_uri
from pydeform.exceptions import (
    ConnectionError,
    ReadTimeout,
)


GLOBALS = {}


def get_setting(name, required=True):
    if name in os.environ:
        try:
            return json.loads(str(os.environ[name]))
        except ValueError:
            raise ValueError(
                "%s should be set in JSON format. Given %s" % (
                    name,
                    os.environ[name]
                )
            )
    else:
        if required:
            raise ValueError(
                'You should provide "%s" environ for settings' % name.upper()
            )

CONFIG = {
    'DEFORM': {
        'HOST': get_setting('DEFORM_HOST'),
        'PORT': get_setting('DEFORM_PORT', required=False),
        'API_BASE_PATH': get_setting(
            'DEFORM_API_BASE_PATH',
            required=False
        ) or '/api/',
        'SECURE': get_setting('DEFORM_SECURE'),
        'PROJECT': get_setting('DEFORM_PROJECT'),
        'PROJECT_NAME': get_setting('DEFORM_PROJECT_NAME'),
        'PROJECT_TOKEN': get_setting('DEFORM_PROJECT_TOKEN'),
        'EMAIL': get_setting('DEFORM_EMAIL'),
        'PASSWORD': get_setting('DEFORM_PASSWORD'),
    },
    'BASE_PATH': os.path.dirname(os.path.normpath(__file__))
}
CONFIG['FILES_PATH'] = os.path.join(CONFIG['BASE_PATH'], 'files')


class TestCase(unittest.TestCase):
    def setUp(self):
        self.CONFIG = CONFIG
        self.requests_session = requests.Session()
        self.request_defaults = {
            'verify': False,
        }


class DeformBaseURITestCaseMixin(object):
    def setUp(self):
        super(DeformBaseURITestCaseMixin, self).setUp()
        self.DEFORM_BASE_URI = get_base_uri(
            host=self.CONFIG['DEFORM']['HOST'],
            api_base_path=self.CONFIG['DEFORM']['API_BASE_PATH'],
            port=self.CONFIG['DEFORM']['PORT'],
            secure=self.CONFIG['DEFORM']['SECURE'],
        )


class DeformClientTestCaseMixin(object):
    def setUp(self):
        super(DeformClientTestCaseMixin, self).setUp()
        self.deform_client = Client(
            host=self.CONFIG['DEFORM']['HOST'],
            port=self.CONFIG['DEFORM']['PORT'],
            secure=self.CONFIG['DEFORM']['SECURE'],
            requests_session=self.requests_session,
            request_defaults=self.request_defaults,
            api_base_path=self.CONFIG['DEFORM']['API_BASE_PATH'],
        )


class DeformSessionAuthClientTestCaseMixin(DeformClientTestCaseMixin):
    def setUp(self):
        super(DeformSessionAuthClientTestCaseMixin, self).setUp()

        if 'deform_session_auth_client' not in GLOBALS:
            GLOBALS['deform_session_auth_client'] = self.deform_client.auth(
                'session',
                self.deform_client.user.login(
                    email=self.CONFIG['DEFORM']['EMAIL'],
                    password=self.CONFIG['DEFORM']['PASSWORD']
                )
            )
        self.deform_session_auth_client = GLOBALS['deform_session_auth_client']


class DeformSessionProjectClientTestCaseMixin(
    DeformSessionAuthClientTestCaseMixin
):
    def setUp(self):
        super(DeformSessionProjectClientTestCaseMixin, self).setUp()

        self.deform_session_project_client = (
            self.deform_session_auth_client.use_project(
                self.CONFIG['DEFORM']['PROJECT']
            )
        )


class DeformTokenProjectClientTestCaseMixin(DeformClientTestCaseMixin):
    def setUp(self):
        super(DeformTokenProjectClientTestCaseMixin, self).setUp()

        if 'deform_token_project_client' not in GLOBALS:
            GLOBALS['deform_token_project_client'] = self.deform_client.auth(
                auth_type='token',
                auth_key=self.CONFIG['DEFORM']['PROJECT_TOKEN'],
                project_id=self.CONFIG['DEFORM']['PROJECT']
            )
        self.deform_token_project_client = GLOBALS[
            'deform_token_project_client'
        ]


def check_timeout(func, kwargs={}):
    experiments = [
        {
            'timeout': 0,
            'exception': ConnectionError,
            'exception_message': 'Connection error'
        },
        {
            'timeout': (0, 100),
            'exception': ConnectionError,
            'exception_message': 'Connection error'
        },
        {
            'timeout': (100, 0),
            'exception': ReadTimeout,
            'exception_message': 'Read timeout'
        },
    ]

    for exp in experiments:
        assert_that(
            calling(func).with_args(timeout=exp['timeout'], **kwargs),
            raises(exp['exception'], exp['exception_message'])
        )
