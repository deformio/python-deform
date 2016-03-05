# -*- coding: utf-8 -*-
from hamcrest import (
    assert_that,
    not_none,
    equal_to,
    instance_of,
    calling,
    raises,
    starts_with,
    has_entry
)

from pydeform import six
from pydeform.client import (
    SessionAuthClient,
    ProjectClient,
)

from testutils import (
    DeformClientTestCaseMixin,
    TestCase,
    DeformSessionAuthClientTestCaseMixin,
    check_timeout
)


class ClientTest__login(DeformClientTestCaseMixin, TestCase):
    def test_login(self):
        response = self.deform_client.login(
            email=self.CONFIG['DEFORM']['EMAIL'],
            password=self.CONFIG['DEFORM']['PASSWORD']
        )
        assert_that(response, instance_of(SessionAuthClient))
        assert_that(response.auth_header, starts_with('SessionId'))


class ClientTest__auth(DeformClientTestCaseMixin, TestCase):
    def test_auth_by_session(self):
        response = self.deform_client.auth(
            auth_type='session',
            auth_key='test'
        )
        assert_that(response, instance_of(SessionAuthClient))
        assert_that(response.auth_header, starts_with('SessionId'))

    def test_auth_by_token_without_project_id(self):
        assert_that(
            calling(self.deform_client.auth).with_args(
                auth_type='token',
                auth_key='test'
            ),
            raises(ValueError, '^You should provide project_id for token authentication$')
        )

    def test_auth_by_token_with_project_id(self):
        response = self.deform_client.auth(
            auth_type='token',
            auth_key='test',
            project_id='some_project'
        )
        assert_that(response, instance_of(ProjectClient))
        assert_that(response.auth_header, starts_with('Token'))


class SessionAuthClientTest__user(DeformSessionAuthClientTestCaseMixin, TestCase):
    def test_get(self):
        response = self.deform_session_auth_client.user.get()
        assert_that(
            response,
            has_entry('email', self.CONFIG['DEFORM']['EMAIL'])
        )
