# -*- coding: utf-8 -*-
from hamcrest import (
    assert_that,
    equal_to,
)

from pydeform.utils import (
    uri_join,
    get_base_uri,
)

from testutils import DeformBaseURITestCaseMixin, TestCase


class Test__uri_join(TestCase):
    def test_dashes(self):
        experiments = [
            {
                'args': ['http://chib.me'],
                'expected': 'http://chib.me'
            },
            {
                'args': ['http://chib.me/'],
                'expected': 'http://chib.me/'
            },
            {
                'args': ['http://chib.me', 'blog'],
                'expected': 'http://chib.me/blog'
            },
            {
                'args': ['http://chib.me/', 'blog'],
                'expected': 'http://chib.me/blog'
            },
            {
                'args': ['http://chib.me/', '/blog'],
                'expected': 'http://chib.me/blog'
            },
            {
                'args': ['http://chib.me/', '/blog/'],
                'expected': 'http://chib.me/blog/'
            },
            {
                'args': ['http://chib.me', '/blog/'],
                'expected': 'http://chib.me/blog/'
            },
            {
                'args': ['http://chib.me', 'blog/'],
                'expected': 'http://chib.me/blog/'
            },
        ]

        for exp in experiments:
            assert_that(uri_join(*exp['args']), equal_to(exp['expected']))

    def test_many_args(self):
        assert_that(
            uri_join('https://chib.me', 'blog', '/my', 'hello/', '/world/'),
            equal_to('https://chib.me/blog/my/hello/world/')
        )

    def test_schema_first(self):
        assert_that(
            uri_join('https://', 'chib.me', 'blog'),
            equal_to('https://chib.me/blog')
        )

class Test__get_base_uri(TestCase):
    def test_me(self):
        api_base_path = self.CONFIG['DEFORM']['API_BASE_PATH']

        experiments = [
            {
                'kwargs': {
                    'host': 'deform.io',
                    'api_base_path': api_base_path
                },
                'expected': uri_join('https://deform.io/', api_base_path)
            },
            {
                'kwargs': {
                    'host': 'deform.io',
                    'project': 'mysquare',
                    'api_base_path': api_base_path
                },
                'expected': uri_join('https://mysquare.deform.io/', api_base_path)
            },
            {
                'kwargs': {
                    'host': 'deform.io',
                    'port': 123,
                    'api_base_path': api_base_path
                },
                'expected': uri_join('https://deform.io:123/', api_base_path)
            },
            {
                'kwargs': {
                    'host': 'deform.io',
                    'secure': False,
                    'api_base_path': api_base_path
                },
                'expected': uri_join('http://deform.io/', api_base_path)
            },
        ]

        for exp in experiments:
            assert_that(
                get_base_uri(**exp['kwargs']),
                equal_to(exp['expected'])
            )
