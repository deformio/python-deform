# -*- coding: utf-8 -*-
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
import responses

from pydeform.utils import (
    uri_join,
    flatten,
)

from pydeform.resources.base import (
    ResourceMethodBase,
)

from testutils import (
    TestCase,
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
                auth_header=self.auth_header,
                requests_session=self.requests_session
            ),
            raises(ValueError, '^You should specify method or action$')
        )

    def test_initialization_with_method(self):
        class ResourceMethod(ResourceMethodBase):
            method = 'get'

        instance = ResourceMethod(
            base_uri=self.base_uri,
            auth_header=self.auth_header,
            requests_session=self.requests_session
        )
        assert_that(instance.method, equal_to('get'))

    def test_initialization_with_action(self):
        class ResourceMethod(ResourceMethodBase):
            action = 'search'

        instance = ResourceMethod(
            base_uri=self.base_uri,
            auth_header=self.auth_header,
            requests_session=self.requests_session,
        )
        assert_that(instance.method, equal_to('post'))
        assert_that(instance.action, equal_to('search'))


class TestResourceMethodBase__get_context(TestCase):
    def setUp(self):
        super(TestResourceMethodBase__get_context, self).setUp()

        self.base_uri = 'http://chib.me/'
        self.auth_header = 'Token 123'

    def get_instance(self, class_):
        return class_(
            base_uri=self.base_uri,
            auth_header=self.auth_header,
            requests_session=self.requests_session,
        )

    def test_simple(self):
        class ResourceMethod(ResourceMethodBase):
            method = 'get'

        instance = self.get_instance(ResourceMethod)
        response = instance.get_context({})
        assert_that(response, has_entry('url', self.base_uri))
        assert_that(response, has_entry('headers', {'Authorization': self.auth_header}))

    def test_simple_action(self):
        class ResourceMethod(ResourceMethodBase):
            action = 'search'

        instance = self.get_instance(ResourceMethod)
        response = instance.get_context({})
        assert_that(response, has_entry('url', self.base_uri))
        assert_that(
            response,
            has_entry('headers', {
                'Authorization': self.auth_header,
                'X-Action': 'search'
            })
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

        instance = self.get_instance(ResourceMethod)
        assert_that(
            instance.get_context({
                'identity': 100,
                'collection': 'users'
            }),
            has_entry('url', uri_join(self.base_uri, 'users', 100, '/'))
        )

        # let's change the order
        instance.uri_params_order = ['identity', 'collection']
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


# todo: teset params_required
