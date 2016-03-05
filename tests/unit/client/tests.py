# -*- coding: utf-8 -*-
from hamcrest import (
    assert_that,
    not_none,
    equal_to,
    instance_of,
    calling,
    raises,
    starts_with,
)

from pydeform import six
from pydeform.client import AuthClient

from testutils import (
    DeformClientTestCaseMixin,
    DeformTokenAuthClientTestCaseMixin,
    TestCase,
    check_timeout
)


class ClientTest__login(DeformClientTestCaseMixin, TestCase):
    def test_login(self):
        response = self.deform_client.login(
            email=self.CONFIG['DEFORM']['EMAIL'],
            password=self.CONFIG['DEFORM']['PASSWORD']
        )
        assert_that(response, instance_of(AuthClient))
        assert_that(response.auth_header, starts_with('Sessionid'))


class ClientTest__auth(DeformClientTestCaseMixin, TestCase):
    def test_auth_by_session(self):
        response = self.deform_client.auth(
            auth_type='session',
            auth_key='test'
        )
        assert_that(response, instance_of(AuthClient))
        assert_that(response.auth_header, starts_with('Sessionid'))

    def test_auth_by_token(self):
        response = self.deform_client.auth(
            auth_type='token',
            auth_key='test'
        )
        assert_that(response, instance_of(AuthClient))
        assert_that(response.auth_header, starts_with('Token'))
