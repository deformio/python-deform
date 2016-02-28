# -*- coding: utf-8 -*-
import datetime
import os

from hamcrest import (
    assert_that,
    not_none,
    equal_to,
    instance_of,
    calling,
    raises,
    starts_with,
    has_entry,
)

from pydeform.utils import (
    format_date,
    format_datetime,
    flatten,
)
from pydeform.resources.utils import (
    get_params_by_destination,
    get_url,
    get_headers,
    get_query_params,
    get_payload,
)

from testutils import (
    TestCase,
)


class ResourcesUtilesTest__get_params_by_destination(TestCase):
    def test_me(self):
        definitions = {
            'one': {
                'name': 'one',
                'dest': 'payload'
            },
            'two': {
                'name': 'two',
                'dest': 'query_params'
            },
            'three': {
                'name': 'three',
                'dest': 'payload'
            },
        }

        params = {
            'one': 'hello',
            'two': 'world',
            'three': 'amigo'
        }

        assert_that(
            get_params_by_destination(
                params=params,
                definitions=definitions,
            ),
            equal_to({
                'payload': {
                    'one': 'hello',
                    'three': 'amigo'
                },
                'query_params': {
                    'two': 'world'
                },
            })
        )


class ResourcesUtilesTest__get_url(TestCase):
    def setUp(self):
        super(ResourcesUtilesTest__get_url, self).setUp()

        self.base_uri = 'https://chib.me/'
        self.uri_params_order = [
            'project',
            'identity',
            'property'
        ]
        self.definitions = {
            'project': {
                'name': 'project',
                'dest': 'uri'
            },
            'identity': {
                'name': 'identity',
                'dest': 'uri',
            },
            'property': {
                'name': 'property',
                'dest': 'uri',
            }
        }

    def test_should_respect_position_with_after(self):
        assert_that(
            get_url(
                base_uri=self.base_uri,
                params={
                    'property': 'three',
                    'project': 'one',
                    'identity': 'two',
                },
                definitions=self.definitions,
                uri_params_order=self.uri_params_order,
            ),
            equal_to('https://chib.me/one/two/three/')
        )

    def test_should_not_fail_if_not_all_after_params_included(self):
        assert_that(
            get_url(
                base_uri=self.base_uri,
                params={
                    'property': 'two',
                    'identity': 'one',
                },
                definitions=self.definitions,
                uri_params_order=self.uri_params_order,
            ),
            equal_to('https://chib.me/one/two/')
        )

    def test_should_convert_lists_to_divided_by_dash_strings(self):
        assert_that(
            get_url(
                base_uri=self.base_uri,
                params={
                    'property': ['four', 'five'],
                    'project': 'one',
                    'identity': ['two', 'three'],
                },
                definitions=self.definitions,
                uri_params_order=self.uri_params_order,
            ),
            equal_to('https://chib.me/one/two/three/four/five/')
        )


class ResourcesUtilesTest__get_headers(TestCase):
    def setUp(self):
        super(ResourcesUtilesTest__get_headers, self).setUp()
        self.auth_header = 'Sessionid hello'

    def test_should_return_auth_header(self):
        assert_that(
            get_headers(
                auth_header=self.auth_header,
                params=None,
                definitions=None
            ),
            has_entry('Authorization', self.auth_header)
        )


class ResourcesUtilesTest__get_query_params(TestCase):
    def setUp(self):
        super(ResourcesUtilesTest__get_query_params, self).setUp()

        self.definitions = {
            'sort': {
                'name': 'sort',
                'dest': 'query_params',
            },
            'fields': {
                'name': 'fields',
                'default': [],
                'dest': 'query_params',
            },
            'fields_exclude': {
                'name': 'fields_exclude',
                'default': [],
                'dest': 'query_params',
            },
        }

    def test_me(self):
        assert_that(
            get_query_params(
                params={
                    'sort': '-name',
                    'fields': ['a', 'b', 'c'],
                    'fields_exclude': ('d', 'e', 'f'),
                },
                definitions=self.definitions
            ),
            equal_to({
                'sort': '-name',
                'fields': 'a,b,c',
                'fields_exclude': 'd,e,f'
            })
        )


class ResourcesUtilesTest__get_payload(TestCase):
    def setUp(self):
        super(ResourcesUtilesTest__get_payload, self).setUp()

        self.definitions = {
            'data': {
                'name': 'data',
                'dest': 'payload',
            }
        }

    def expect_response(self, value, expected, type_='json'):
        experiments = [
            {
                'value': value,
                'expected': expected
            },
            {
                'value': [1, 2, value],
                'expected': [1, 2, expected]
            },
            {
                'value': (1, 2, value),
                'expected': (1, 2, expected)
            },
            {
                'value': {
                    'key': value
                },
                'expected': {
                    'key': expected
                }
            },
            {
                'value': {
                    'key': (0, 1, value)
                },
                'expected': {
                    'key': (0, 1, expected)
                }
            },
        ]

        for exp in experiments:
            expected_prepared = exp['expected']
            if type_ == 'files':
                expected_prepared = flatten(expected_prepared)
            assert_that(
                get_payload(
                    params={
                        'data': exp['value']
                    },
                    definitions=self.definitions
                ),
                equal_to({
                    'type': type_,
                    'data': expected_prepared
                })
            )

    def test_none(self):
        self.expect_response(None, None)

    def test_strings(self):
        self.expect_response('hello', 'hello')
        self.expect_response(u'Привет', u'Привет')

    def test_int(self):
        self.expect_response(1, 1)

    def test_float(self):
        self.expect_response(1.12, 1.12)

    def test_date(self):
        date = datetime.date(year=1990, month=3, day=2)
        self.expect_response(date, format_date(date))

    def test_datetime(self):
        value = datetime.datetime(
            year=1990,
            month=3,
            day=2,
            hour=10,
            minute=9,
            second=8
        )
        self.expect_response(value, format_datetime(value))

    def test_file(self):
        value = open(os.path.join(self.CONFIG['FILES_PATH'], '1.txt'))
        self.expect_response(value, value, type_='files')
