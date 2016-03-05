# -*- coding: utf-8 -*-
from hamcrest import (
    assert_that,
    not_none,
    equal_to,
    instance_of,
    calling,
    raises,
    starts_with,
    has_entry,
    is_not,
    empty
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


class SessionAuthClientTest__projects(DeformSessionAuthClientTestCaseMixin, TestCase):
    def test_get(self):
        response = self.deform_session_auth_client.projects.all()
        projects = [i for i in response]
        assert_that(projects, is_not([]))

    def test_find(self):
        response = self.deform_session_auth_client.projects.find(
            filter={'name': self.CONFIG['DEFORM']['PROJECT_NAME']}
        )
        projects = [i for i in response]
        assert_that(projects, is_not([]))
        assert_that(
            projects[0],
            has_entry('_id', self.CONFIG['DEFORM']['PROJECT']),
            has_entry('name', self.CONFIG['DEFORM']['PROJECT_NAME']),
        )

    def test_find__full_text(self):
        response = self.deform_session_auth_client.projects.find(
            text=self.CONFIG['DEFORM']['PROJECT_NAME']
        )
        projects = [i for i in response]
        assert_that(projects, is_not([]))
        assert_that(
            projects[0],
            has_entry('_id', self.CONFIG['DEFORM']['PROJECT']),
            has_entry('name', self.CONFIG['DEFORM']['PROJECT_NAME']),
        )


class SessionAuthClientTest__project(DeformSessionAuthClientTestCaseMixin, TestCase):
    def test_get(self):
        response = self.deform_session_auth_client.project.get(
            identity=self.CONFIG['DEFORM']['PROJECT']
        )
        assert_that(
            response,
            has_entry('_id', self.CONFIG['DEFORM']['PROJECT']),
            has_entry('name', self.CONFIG['DEFORM']['PROJECT_NAME']),
        )

    def _test_save(self):
        response = self.deform_session_auth_client.project.get(
            identity=self.CONFIG['DEFORM']['PROJECT']
        )
        assert_that(
            response,
            has_entry('_id', self.CONFIG['DEFORM']['PROJECT']),
            has_entry('name', self.CONFIG['DEFORM']['PROJECT_NAME']),
        )
