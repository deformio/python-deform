# -*- coding: utf-8 -*-
from hamcrest import assert_that, equal_to
from pydeform.utils import flatten, get_base_uri, uri_join
from testutils import TestCase


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
            {
                'args': ['http://chib.me', 'hello amigo', '/blog/'],
                'expected': 'http://chib.me/hello+amigo/blog/'
            },
            {
                'args': ['http://chib.me', 1, 2, 3],
                'expected': 'http://chib.me/1/2/3'
            },
            {
                'args': ['http://chib.me', '/last-slash', '/'],
                'expected': 'http://chib.me/last-slash/'
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
                'expected': uri_join(
                    'https://mysquare.deform.io/',
                    api_base_path
                )
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


class Test__flatten(TestCase):
    def test_string(self):
        assert_that(
            flatten('hello'),
            equal_to('hello')
        )

    def test_none(self):
        assert_that(
            flatten(None),
            equal_to(None)
        )

    def test_empty_dict(self):
        assert_that(
            flatten({}),
            equal_to({})
        )

    def test_empty_list(self):
        assert_that(
            flatten([]),
            equal_to([])
        )

    def test_empty_tuple(self):
        assert_that(
            flatten(tuple()),
            equal_to(tuple())
        )

    def test_dict_with_simple_key(self):
        assert_that(
            flatten({'name': 'gena', 'surname': 'chibisov'}),
            equal_to({'name': 'gena', 'surname': 'chibisov'})
        )

    def test_list_with_simple_values(self):
        assert_that(
            flatten(['gena', 'vova']),
            equal_to({
                '[0]': 'gena',
                '[1]': 'vova',
            })
        )

    def test_tuple_with_simple_values(self):
        assert_that(
            flatten(('gena', 'vova')),
            equal_to({
                '[0]': 'gena',
                '[1]': 'vova',
            })
        )

    def test_dict_with_dict_values(self):
        assert_that(
            flatten({
                'user': {
                    'name': 'gena',
                    'surname': 'chibisov'
                }
            }),
            equal_to({
                'user.name': 'gena',
                'user.surname': 'chibisov',
            })
        )

    def test_dict_with_list_values(self):
        assert_that(
            flatten({
                'users': ['gena', 'vova']
            }),
            equal_to({
                'users[0]': 'gena',
                'users[1]': 'vova',
            })
        )

    def test_list_with_dict_value(self):
        assert_that(
            flatten({
                'users': [
                    {
                        'name': 'gena',
                        'surname': 'chibisov'
                    },
                    {
                        'name': 'vova',
                        'surname': 'ivanov'
                    }
                ]
            }),
            equal_to({
                'users[0].name': 'gena',
                'users[0].surname': 'chibisov',
                'users[1].name': 'vova',
                'users[1].surname': 'ivanov',
            })
        )

    def test_list_with_list_value(self):
        assert_that(
            flatten({
                'users': [
                    [
                        'gena',
                        'vova'
                    ],
                    [
                        'max',
                        'oleg'
                    ]
                ]
            }),
            equal_to({
                'users[0][0]': 'gena',
                'users[0][1]': 'vova',
                'users[1][0]': 'max',
                'users[1][1]': 'oleg',
            })
        )

    def test_complex(self):
        assert_that(
            flatten({
                'users': [
                    {
                        'name': 'gena',
                        'surname': 'chibisov',
                        'groups': ['admin', 'superuser']
                    },
                    {
                        'name': 'vova',
                        'surname': 'ivanov',
                        'groups': ['user']
                    },
                    {
                        'name': 'ivan',
                        'surname': 'petrov',
                        'groups': []
                    },
                ],
                'groups': {
                    'admin': {
                        'name': 'Admin',
                        'grants': ['remove', 'create']
                    },
                    'superuser': {
                        'name': 'Super user',
                        'grants': ['all']
                    },
                    'user': {
                        'name': 'User',
                        'grants': []
                    }
                }
            }),
            equal_to({
                'users[0].name': 'gena',
                'users[0].surname': 'chibisov',
                'users[0].groups[0]': 'admin',
                'users[0].groups[1]': 'superuser',

                'users[1].name': 'vova',
                'users[1].surname': 'ivanov',
                'users[1].groups[0]': 'user',

                'users[2].name': 'ivan',
                'users[2].surname': 'petrov',
                'users[2].groups': [],

                'groups.admin.name': 'Admin',
                'groups.admin.grants[0]': 'remove',
                'groups.admin.grants[1]': 'create',

                'groups.superuser.name': 'Super user',
                'groups.superuser.grants[0]': 'all',

                'groups.user.name': 'User',
                'groups.user.grants': [],
            })
        )
