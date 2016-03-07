# -*- coding: utf-8 -*-
import datetime
import os
import types

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
import responses

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
    prepare_payload,
    iterate_by_pagination,
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
        self.definitions = {
            'collection': {
                'name': 'collection',
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

    def test_me(self):
        assert_that(
            get_url(
                base_uri=self.base_uri,
                path=[
                    'collections',
                    '{collection}',
                    'documents',
                    '{should_skip_me_because_no_such_param}',
                    '{identity}',
                    '{property}'
                ],
                params={
                    'property': ['four', 'five'],
                    'collection': '_users',
                    'identity': 'someid',
                },
                definitions=self.definitions,
            ),
            equal_to('https://chib.me/collections/_users/documents/someid/four/five/')
        )


class ResourcesUtilesTest__get_headers(TestCase):
    def setUp(self):
        super(ResourcesUtilesTest__get_headers, self).setUp()
        self.auth_header = 'SessionId hello'

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


class ResourcesUtilesTest__prepare_payload(TestCase):
    def expect_response(self, value, expected, with_files=False):
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
            assert_that(
                prepare_payload(exp['value']),
                equal_to((with_files, exp['expected']))
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
        self.expect_response(value, value, with_files=True)


class ResourcesUtilesTest__get_payload(TestCase):
    def setUp(self):
        super(ResourcesUtilesTest__get_payload, self).setUp()

        self.definitions = {
            'data': {
                'name': 'data',
                'dest': 'payload',
            },
            'find_filter': {
                'dest': 'payload',
                'payload_property': 'filter',
                'description': 'Filter query'
            },
            'find_text': {
                'dest': 'payload',
                'payload_property': 'text',
                'description': 'Full text search value'
            },
        }

    def test_no_params(self):
        for i in [None, {}]:
            assert_that(
                get_payload(i, self.definitions),
                equal_to(None)
            )

    def test_full_payload_param(self):
        assert_that(
            get_payload({'data': {'some': 'value'}}, self.definitions),
            equal_to({
                'type': 'json',
                'data': {
                    'payload': {'some': 'value'}
                }
            })
        )

    def test_payload_property_params(self):
        assert_that(
            get_payload(
                {
                    'find_filter': {
                        'some': 'value'
                    },
                    'find_text': {
                        'another_some': 'another_value'
                    },
                },
                self.definitions
            ),
            equal_to({
                'type': 'json',
                'data': {
                    'payload': {
                        'filter': {
                            'some': 'value',
                        },
                        'text': {
                            'another_some': 'another_value',
                        }
                    }
                }
            })
        )

    def test_params_with_files(self):
        params = {
            'data': {
                'user': {
                    'name': 'gena'
                },
                'avatar': {
                    'big': open(os.path.join(self.CONFIG['FILES_PATH'], '1.txt'))
                }
            }
        }
        assert_that(
            get_payload(params, self.definitions),
            equal_to({
                'type': 'files',
                'data': flatten(prepare_payload(params['data'])[1])
            })
        )


class ResourcesUtilesTest__iterate_by_pagination(TestCase):
    def setUp(self):
        super(ResourcesUtilesTest__iterate_by_pagination, self).setUp()

        self.method = 'GET'
        self.url = 'http://chib.me/users/'
        self.request_kwargs = {
            'url': self.url
        }

    def get_list_from_generator(self, generator):
        return [i for i in generator]

    @responses.activate
    def test_should_return_generator(self):
        responses.add(
            self.method,
            self.url,
            json={
                'links': {},
                'results': []
            }
        )

        assert_that(
            iterate_by_pagination(
                method=self.method,
                request_kwargs=self.request_kwargs,
                requests_session=self.requests_session,
                request_defaults=self.request_defaults
            ),
            instance_of(types.GeneratorType)
        )

    @responses.activate
    def test_one_page(self):
        results = [
            1,
            2,
            3
        ]
        responses.add(
            self.method,
            self.url,
            json={
                'links': {},
                'result': results
            }
        )

        response = iterate_by_pagination(
            method=self.method,
            request_kwargs=self.request_kwargs,
            requests_session=self.requests_session,
            request_defaults=self.request_defaults
        )
        assert_that(
            self.get_list_from_generator(response),
            equal_to(results)
        )

    @responses.activate
    def test_two_pages(self):
        page_1_results = [
            1,
            2,
            3
        ]
        page_2_results = [
            1,
            2,
            3
        ]
        responses.add(
            self.method,
            self.url + '?page=1',
            json={
                'links': {
                    'next': 'http://next/blablabla'
                },
                'result': page_1_results
            },
            match_querystring=True
        )
        responses.add(
            self.method,
            self.url + '?page=2',
            json={
                'links': {},
                'result': page_2_results
            },
            match_querystring=True
        )

        response = iterate_by_pagination(
            method=self.method,
            request_kwargs=self.request_kwargs,
            requests_session=self.requests_session,
            request_defaults=self.request_defaults
        )
        assert_that(
            self.get_list_from_generator(response),
            equal_to(page_1_results + page_2_results)
        )

    @responses.activate
    def test_one_page_not_found(self):
        responses.add(
            self.method,
            self.url,
            json={'error': 'Not found'},
            status=404
        )

        response = iterate_by_pagination(
            method=self.method,
            request_kwargs=self.request_kwargs,
            requests_session=self.requests_session,
            request_defaults=self.request_defaults
        )
        assert_that(
            self.get_list_from_generator(response),
            equal_to([])
        )

    @responses.activate
    def test_second_page_not_found(self):
        page_1_results = [
            1,
            2,
            3
        ]
        responses.add(
            self.method,
            self.url + '?page=1',
            json={
                'links': {
                    'next': 'http://next/blablabla'
                },
                'result': page_1_results
            },
            match_querystring=True
        )
        responses.add(
            self.method,
            self.url + '?page=2',
            json={
                'error': 'Not found',
            },
            status=404,
            match_querystring=True
        )

        response = iterate_by_pagination(
            method=self.method,
            request_kwargs=self.request_kwargs,
            requests_session=self.requests_session,
            request_defaults=self.request_defaults
        )
        assert_that(
            self.get_list_from_generator(response),
            equal_to(page_1_results)
        )

    @responses.activate
    def test_second_page_is_empty(self):
        page_1_results = [
            1,
            2,
            3
        ]
        responses.add(
            self.method,
            self.url + '?page=1',
            json={
                'links': {
                    'next': 'http://next/blablabla'
                },
                'result': page_1_results
            },
            match_querystring=True
        )
        responses.add(
            self.method,
            self.url + '?page=2',
            json={
                'links': {},
                'result': []
            },
            match_querystring=True
        )

        response = iterate_by_pagination(
            method=self.method,
            request_kwargs=self.request_kwargs,
            requests_session=self.requests_session,
            request_defaults=self.request_defaults
        )
        assert_that(
            self.get_list_from_generator(response),
            equal_to(page_1_results)
        )
