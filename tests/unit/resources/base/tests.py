# -*- coding: utf-8 -*-
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
    has_entries,
)
import responses
from mock import Mock

from pydeform.utils import (
    uri_join,
    flatten,
)

from pydeform.resources.base import (
    ResourceMethodBase,
)

from testutils import (
    TestCase,
    check_timeout
)


class TestResourceMethodBase__initialization(TestCase):
    def setUp(self):
        super(TestResourceMethodBase__initialization, self).setUp()

        self.base_uri = 'http://chib.me/'
        self.auth_header = 'Token 123'

    def test_should_force_to_initialize_method_or_action(self):
        assert_that(
            calling(ResourceMethodBase).with_args(
                base_uri=self.base_uri,
                path=[],
                auth_header=self.auth_header,
                requests_session=self.requests_session,
                request_defaults=self.request_defaults,
            ),
            raises(ValueError, '^You should specify method or action$')
        )

    def test_initialization_with_method(self):
        class ResourceMethod(ResourceMethodBase):
            method = 'get'

        instance = ResourceMethod(
            base_uri=self.base_uri,
            path=[],
            auth_header=self.auth_header,
            requests_session=self.requests_session,
            request_defaults=self.request_defaults
        )
        assert_that(instance.method, equal_to('get'))

    def test_initialization_with_action(self):
        class ResourceMethod(ResourceMethodBase):
            action = 'find'

        instance = ResourceMethod(
            base_uri=self.base_uri,
            path=[],
            auth_header=self.auth_header,
            requests_session=self.requests_session,
            request_defaults=self.request_defaults
        )
        assert_that(instance.method, equal_to('post'))
        assert_that(instance.action, equal_to('find'))


class TestResourceMethodBase__get_context(TestCase):
    def setUp(self):
        super(TestResourceMethodBase__get_context, self).setUp()

        self.base_uri = 'http://chib.me/'
        self.auth_header = 'Token 123'

    def get_instance(self, class_, path=[]):
        return class_(
            base_uri=self.base_uri,
            path=path,
            auth_header=self.auth_header,
            requests_session=self.requests_session,
            request_defaults=self.request_defaults
        )

    def test_simple(self):
        class ResourceMethod(ResourceMethodBase):
            method = 'get'

        instance = self.get_instance(ResourceMethod)
        response = instance.get_context({})
        assert_that(response, has_entry('url', self.base_uri))
        assert_that(
            response,
            has_entry(
                'headers',
                has_entries({
                    'Authorization': self.auth_header,
                    'Content-Type': 'application/json'
                })
            )
        )

    def test_simple_action(self):
        class ResourceMethod(ResourceMethodBase):
            action = 'find'

        instance = self.get_instance(ResourceMethod)
        response = instance.get_context({})
        assert_that(response, has_entry('url', self.base_uri))
        assert_that(
            response,
            has_entry(
                'headers',
                has_entries({
                    'Authorization': self.auth_header,
                    'X-Action': 'find',
                    'Content-Type': 'application/json'
                })
            )
        )

    def test_with_uri_params_defined(self):
        class ResourceMethod(ResourceMethodBase):
            method = 'get'
            params = {
                'collection': {
                    'dest': 'uri'
                },
                'identity': {
                    'dest': 'uri'
                },
            }
            uri_params_order = ['collection', 'identity']

        instance = self.get_instance(ResourceMethod, path=['{collection}', '{identity}'])
        assert_that(
            instance.get_context({
                'identity': 100,
                'collection': 'users'
            }),
            has_entry('url', uri_join(self.base_uri, 'users', 100, '/'))
        )

        # let's change the order
        instance = self.get_instance(ResourceMethod, path=['{identity}', '{collection}'])
        assert_that(
            instance.get_context({
                'identity': 100,
                'collection': 'users'
            }),
            has_entry('url', uri_join(self.base_uri, 100, 'users', '/'))
        )

    def test_with_query_params_defined(self):
        class ResourceMethod(ResourceMethodBase):
            method = 'get'
            params = {
                'fields': {
                    'dest': 'query_params'
                },
                'fields_exclude': {
                    'dest': 'query_params'
                },
            }

        instance = self.get_instance(ResourceMethod)
        assert_that(
            instance.get_context({
                'fields': ['name', 'surname'],
                'fields_exclude': ['age', 'avatar']
            }),
            has_entry(
                'params',
                {
                    'fields': 'name,surname',
                    'fields_exclude': 'age,avatar',
                }
            )
        )

    def test_with_payload_params(self):
        class ResourceMethod(ResourceMethodBase):
            method = 'get'
            params = {
                'data': {
                    'dest': 'payload'
                },
            }

        instance = self.get_instance(ResourceMethod)
        assert_that(
            instance.get_context({
                'data': {
                    'user': {
                        'name': 'gena'
                    }
                },
            }),
            has_entry(
                'json',
                {
                    'payload': {
                        'user': {
                            'name': 'gena'
                        }
                    }
                }
            )
        )

        # with files
        data = {
            'user': {
                'name': 'gena',
                'avatar': open(os.path.join(self.CONFIG['FILES_PATH'], '1.txt'))
            }
        }
        assert_that(
            instance.get_context({
                'data': data,
            }),
            has_entry('files', flatten(data))
        )



class TestResourceMethodBase__call(TestCase):
    def setUp(self):
        super(TestResourceMethodBase__call, self).setUp()

        self.base_uri = 'http://chib.me/'
        self.auth_header = 'Token 123'
        self.method = 'GET'

    def get_instance(self, class_, path=[]):
        instance = class_(
            base_uri=self.base_uri,
            path=path,
            auth_header=self.auth_header,
            requests_session=self.requests_session,
            request_defaults=self.request_defaults
        )
        return instance

    @responses.activate
    def test_should_raise_error_if_required_param_not_sent(self):
        class ResourceMethod(ResourceMethodBase):
            method = 'get'
            params = {
                'name': {
                    'dest': 'query_params'
                },
                'surname': {
                    'dest': 'query_params'
                }
            }
            params_required = ['surname']

        instance = self.get_instance(ResourceMethod)
        assert_that(
            calling(instance).with_args(name='gena'),
            raises(ValueError, '^surname is required parameter$')
        )

    @responses.activate
    def test_should_raise_error_if_required_param_not_sent(self):
        class ResourceMethod(ResourceMethodBase):
            method = 'get'
            params = {
                'name': {
                    'dest': 'query_params'
                },
                'surname': {
                    'dest': 'query_params'
                }
            }
            params_required = ['surname']

        instance = self.get_instance(ResourceMethod)
        assert_that(
            calling(instance).with_args(name='gena'),
            raises(ValueError, '^surname is required parameter$')
        )

    @responses.activate
    def test_should_return_result_response(self):
        class ResourceMethod(ResourceMethodBase):
            method = 'get'
            params = {
                'name': {
                    'dest': 'query_params'
                },
                'surname': {
                    'dest': 'query_params'
                },
            }
            params_required = ['surname']

        responses.add(
            self.method,
            self.base_uri,
            json={
                'result': {
                    'age': 26
                }
            }
        )

        instance = self.get_instance(ResourceMethod)
        assert_that(
            instance(name='gena', surname='chibisov'),
            equal_to({'age': 26})
        )

    @responses.activate
    def test_should_none_if_response_body_is_empty(self):
        class ResourceMethod(ResourceMethodBase):
            method = 'get'

        responses.add(
            self.method,
            self.base_uri,
            body=''
        )

        instance = self.get_instance(ResourceMethod)
        assert_that(
            instance(),
            equal_to(None)
        )

    @responses.activate
    def test_should_return_generator_if_paginatable(self):
        class ResourceMethod(ResourceMethodBase):
            method = 'get'
            params = {
                'name': {
                    'dest': 'query_params'
                },
                'surname': {
                    'dest': 'query_params'
                },
            }
            is_paginatable = True
            params_required = ['surname']

        page_1_result = [1, 2, 3]
        page_2_result = [4, 5, 6]
        responses.add(
            self.method,
            self.base_uri + '?page=1&name=gena&surname=chibisov',
            json={
                'links': {
                    'next': 'http://next'
                },
                'result': page_1_result
            },
            match_querystring=True
        )
        responses.add(
            self.method,
            self.base_uri + '?page=2&name=gena&surname=chibisov',
            json={
                'result': page_2_result
            },
            match_querystring=True
        )

        instance = self.get_instance(ResourceMethod)
        response = instance(name='gena', surname='chibisov')
        assert_that(response, instance_of(types.GeneratorType))
        assert_that(
            [i for i in response],
            equal_to(page_1_result + page_2_result)
        )

    @responses.activate
    def test_should_return_page_if_paginatable_and_pagination_param_has_been_sent(self):
        class ResourceMethod(ResourceMethodBase):
            method = 'get'
            params = {
                'name': {
                    'dest': 'query_params'
                },
                'surname': {
                    'dest': 'query_params'
                },
            }
            is_paginatable = True
            params_required = ['surname']

        instance = self.get_instance(ResourceMethod)

        page_1_result = [1, 2, 3]
        page_2_result = [4, 5, 6]
        responses.add(
            self.method,
            self.base_uri + '?page=1&name=gena&surname=chibisov',
            json={
                'links': {
                    'next': 'http://next'
                },
                'result': page_1_result
            },
            match_querystring=True
        )
        responses.add(
            self.method,
            self.base_uri + '?page=2&name=gena&surname=chibisov',
            json={
                'page': 2,
                'pages': 10,
                'per_page': 20,
                'total': 30,
                'result': page_2_result,
                'another_key_that_should_not_be_in_response': 'noooooo'
            },
            match_querystring=True
        )

        # page param
        assert_that(
            instance(name='gena', surname='chibisov', page=2),
            equal_to({
                'page': 2,
                'pages': 10,
                'per_page': 20,
                'total': 30,
                'result': page_2_result,
            })
        )

        # per_page param
        per_page_result = [10, 20, 30]
        responses.add(
            self.method,
            self.base_uri + '?name=gena&surname=chibisov&per_page=33',
            json={
                'page': 2,
                'pages': 10,
                'per_page': 20,
                'total': 30,
                'result': per_page_result,
                'another_key_that_should_not_be_in_response': 'noooooo'
            },
            match_querystring=True
        )
        assert_that(
            instance(name='gena', surname='chibisov', per_page=33),
            equal_to({
                'page': 2,
                'pages': 10,
                'per_page': 20,
                'total': 30,
                'result': per_page_result,
            })
        )

        # page and per_page param
        page_and_per_page_result = [100, 200, 300]
        responses.add(
            self.method,
            self.base_uri + '?page=5&name=gena&surname=chibisov&per_page=33',
            json={
                'page': 2,
                'pages': 10,
                'per_page': 20,
                'total': 30,
                'result': page_and_per_page_result,
                'another_key_that_should_not_be_in_response': 'noooooo'
            },
            match_querystring=True
        )
        assert_that(
            instance(name='gena', surname='chibisov', per_page=33, page=5),
            equal_to({
                'page': 2,
                'pages': 10,
                'per_page': 20,
                'total': 30,
                'result': page_and_per_page_result,
            })
        )

    @responses.activate
    def test_with_return_create_status(self):
        class ResourceMethod(ResourceMethodBase):
            method = 'put'
            return_create_status = True

        responses.add(
            'PUT',
            self.base_uri,
            json={
                'result': 'world',
            },
            status=201
        )
        instance = self.get_instance(ResourceMethod)
        assert_that(
            instance(),
            equal_to({
                'created': True,
                'result': 'world'
            })
        )

        # test when not created
        responses.reset()
        responses.add(
            'PUT',
            self.base_uri,
            json={
                'result': 'world',
            },
            status=200
        )
        assert_that(
            instance(),
            equal_to({
                'created': False,
                'result': 'world'
            })
        )

    def test_for_timeout(self):
        class ResourceMethod(ResourceMethodBase):
            method = 'get'

        instance = self.get_instance(ResourceMethod)
        check_timeout(instance)
