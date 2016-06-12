# -*- coding: utf-8 -*-
import responses
from hamcrest import (
    assert_that,
    calling,
    equal_to,
    has_entry,
    instance_of,
    is_not,
    raises
)
from pydeform.client import ProjectClient
from pydeform.exceptions import AuthError
from pydeform.utils import get_base_uri
from testutils import DeformSessionAuthClientTestCaseMixin, TestCase


class SessionAuthClientTest__user(
    DeformSessionAuthClientTestCaseMixin,
    TestCase
):
    def test_get(self):
        response = self.deform_session_auth_client.user.get()
        assert_that(
            response,
            has_entry('email', self.CONFIG['DEFORM']['EMAIL'])
        )

    def test_logout(self):
        deform_session_auth_client = self.deform_client.auth(
            'session',
            self.deform_client.user.login(
                email=self.CONFIG['DEFORM']['EMAIL'],
                password=self.CONFIG['DEFORM']['PASSWORD']
            )
        )
        response = deform_session_auth_client.user.logout()
        assert_that(response, equal_to(None))
        assert_that(
            calling(deform_session_auth_client.user.get),
            raises(AuthError, '^Not authorized$')
        )

    def test_update(self):
        with responses.RequestsMock() as rsps:
            rsps.add(
                self.deform_session_auth_client.user.update.method.upper(),
                self.deform_session_auth_client.user.update.get_context(
                    {}
                )['url'],
                json={
                    'result': {
                        'email': self.CONFIG['DEFORM']['EMAIL']
                    }
                },
                status=200
            )
            self.deform_session_auth_client.user.update(data={'some': 'data'})


class SessionAuthClientTest__projects(
    DeformSessionAuthClientTestCaseMixin,
    TestCase
):
    def test_find_is_paginatable(self):
        assert_that(
            self.deform_session_auth_client.projects.find.is_paginatable,
            equal_to(True)
        )

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

    def test_find_sort(self):
        response_1 = self.deform_session_auth_client.projects.find(
            sort=['_id']
        )
        response_1 = [i for i in response_1]
        response_2 = self.deform_session_auth_client.projects.find(
            sort=['-_id']
        )
        response_2 = [i for i in response_2]
        for i, item in enumerate(response_1):
            j = (i + 1) * -1
            assert_that(
                item,
                equal_to(response_2[j]),
                'item %s and %s does not equal' % (i, j)
            )

    def test_count(self):
        response = self.deform_session_auth_client.projects.count()
        expected = self.deform_session_auth_client.projects.find(
            per_page=1
        )['total']
        assert_that(response, equal_to(expected))

    def test_count__filter(self):
        response = self.deform_session_auth_client.projects.count(
            filter={'name': self.CONFIG['DEFORM']['PROJECT_NAME']}
        )
        assert_that(response, equal_to(1))

    def test_count__full_text(self):
        response = self.deform_session_auth_client.projects.count(
            filter={
                'name': self.CONFIG['DEFORM']['PROJECT_NAME'],
            },
            text=self.CONFIG['DEFORM']['PROJECT_NAME']
        )
        assert_that(response, equal_to(1))


class SessionAuthClientTest__project(
    DeformSessionAuthClientTestCaseMixin,
    TestCase
):
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
            self.deform_session_auth_client.project.create.get_context(
                {}
            )['url'],
            json={
                '_id': 'new-project',
                'name': 'New project'
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


class SessionAuthClientTest__use_project(
    DeformSessionAuthClientTestCaseMixin,
    TestCase
):
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
