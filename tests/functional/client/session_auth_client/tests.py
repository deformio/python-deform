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
import responses

from pydeform import six
from pydeform.client import (
    SessionAuthClient,
    ProjectClient,
)
from pydeform.utils import get_base_uri

from testutils import (
    DeformClientTestCaseMixin,
    TestCase,
    DeformSessionAuthClientTestCaseMixin,
    check_timeout
)


class SessionAuthClientTest__user(DeformSessionAuthClientTestCaseMixin, TestCase):
    def test_get(self):
        response = self.deform_session_auth_client.user.get()
        assert_that(
            response,
            has_entry('email', self.CONFIG['DEFORM']['EMAIL'])
        )


class SessionAuthClientTest__projects(DeformSessionAuthClientTestCaseMixin, TestCase):
    def test_find(self):
        response = self.deform_session_auth_client.projects.find()
        projects = [i for i in response]
        assert_that(projects, is_not([]))

    def test_find__with_filter(self):
        response = self.deform_session_auth_client.projects.find(
            filter={'name': self.CONFIG['DEFORM']['PROJECT_NAME']}
        )
        projects = [i for i in response]
        assert_that(projects, is_not([]))
        assert_that(
            projects[0],
            has_entry('_id', self.CONFIG['DEFORM']['PROJECT']),
        )
        assert_that(
            projects[0],
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
        )
        assert_that(
            projects[0],
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
        )
        assert_that(
            response,
            has_entry('name', self.CONFIG['DEFORM']['PROJECT_NAME']),
        )

    def test_save(self):
        response = self.deform_session_auth_client.project.save(
            identity=self.CONFIG['DEFORM']['PROJECT'],
            data={
                'name': self.CONFIG['DEFORM']['PROJECT_NAME']
            }
        )
        assert_that(response['created'], equal_to(False))
        assert_that(
            response['result'],
            has_entry('_id', self.CONFIG['DEFORM']['PROJECT']),
        )
        assert_that(
            response['result'],
            has_entry('name', self.CONFIG['DEFORM']['PROJECT_NAME']),
        )

    @responses.activate
    def test_create(self):
        responses.add(
            self.deform_session_auth_client.project.create.method.upper(),
            self.deform_session_auth_client.project.create.get_context({})['url'],
            json={
                'result': {
                    '_id': 'new-project',
                    'name': 'New project'
                }
            },
            status=201
        )

        response = self.deform_session_auth_client.project.create(data={
            '_id': 'new-project',
            'name': 'New project'
        })
        assert_that(response, equal_to({
            '_id': 'new-project',
            'name': 'New project'
        }))


class SessionAuthClientTest__use_project(DeformSessionAuthClientTestCaseMixin, TestCase):
    def test_me(self):
        response = self.deform_session_auth_client.use_project('some-project')
        assert_that(response, instance_of(ProjectClient))
        assert_that(
            response.base_uri,
            equal_to(get_base_uri(
                project='some-project',
                host=self.deform_session_auth_client.host,
                port=self.deform_session_auth_client.port,
                secure=self.deform_session_auth_client.secure,
                api_base_path=self.deform_session_auth_client.api_base_path
            ))
        )
        assert_that(
            response.auth_header,
            equal_to(self.deform_session_auth_client.auth_header)
        )
