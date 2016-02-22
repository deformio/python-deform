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

from pydeform.utils import get_base_uri
from pydeform.exceptions import (
    ConnectionError,
    ReadTimeout,
)


def get_setting(name, required=True):
    if name in os.environ:
        try:
            return json.loads(str(os.environ[name]))
        except ValueError as e:
            raise ValueError("%s should be set in JSON format. Given %s" % (name, os.environ[name]))
    else:
        if required:
            raise ValueError('You should provide "%s" environ for settings' % name.upper())

CONFIG = {
    'DEFORM': {
        'HOST': get_setting('DEFORM_HOST'),
        'PORT': get_setting('DEFORM_PORT', required=False),
        'API_BASE_PATH': get_setting('DEFORM_API_BASE_PATH', required=False) or '/api/',
        'SECURE': get_setting('DEFORM_SECURE'),
        # 'PROJECT': get_setting('DEFORM_PROJECT'),
        'EMAIL': get_setting('DEFORM_EMAIL'),
        'PASSWORD': get_setting('DEFORM_PASSWORD'),
    }
}

class TestCase(unittest.TestCase):
    def setUp(self):
        self.CONFIG = CONFIG
        self.requests_session = requests.Session()


class DeformBaseURITestCaseMixin(object):
    def setUp(self):
        super(DeformBaseURITestCaseMixin, self).setUp()
        self.DEFORM_BASE_URI = get_base_uri(
            host=self.CONFIG['DEFORM']['HOST'],
            api_base_path=self.CONFIG['DEFORM']['API_BASE_PATH'],
            port=self.CONFIG['DEFORM']['PORT'],
            secure=self.CONFIG['DEFORM']['SECURE'],
        )


def check_timeout(func, kwargs):
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
