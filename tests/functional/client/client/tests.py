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
from pydeform.exceptions import (
    NotFoundError,
    AuthError,
    ConflictError,
)

from testutils import (
    DeformClientTestCaseMixin,
    TestCase,
)


class ClientTest__user(DeformClientTestCaseMixin, TestCase):
    def test_login(self):
        response = self.deform_client.user.login(
            email=self.CONFIG['DEFORM']['EMAIL'],
            password=self.CONFIG['DEFORM']['PASSWORD']
        )
        assert_that(response, instance_of(six.text_type))

    def test_login__email_not_exists(self):
        assert_that(
            calling(self.deform_client.user.login).with_args(
                email='a' + self.CONFIG['DEFORM']['EMAIL'],
                password=self.CONFIG['DEFORM']['PASSWORD']
            ),
            raises(AuthError, '^Wrong credentials provided\.$')
        )

    def test_login__wrong_password(self):
        assert_that(
            calling(self.deform_client.user.login).with_args(
                email=self.CONFIG['DEFORM']['EMAIL'],
                password='a' + self.CONFIG['DEFORM']['PASSWORD']
            ),
            raises(AuthError, '^Wrong credentials provided\.$')
        )

    def test_create_new_user(self):
        with responses.RequestsMock() as rsps:
            rsps.add(
                self.deform_client.user.create.method.upper(),
                self.deform_client.user.create.get_context({})['url'],
                json={
                    'result': {
                        'message': 'Check your email for confirmation code'
                    }
                },
                status=201
            )
            response = self.deform_client.user.create(
                email='a' + self.CONFIG['DEFORM']['EMAIL'],
                password=self.CONFIG['DEFORM']['PASSWORD']
            )
            assert_that(
                response,
                has_entry('message', 'Check your email for confirmation code')
            )

    def test_create_user_with_existing_email(self):
        assert_that(
            calling(self.deform_client.user.create).with_args(
                email=self.CONFIG['DEFORM']['EMAIL'],
                password=self.CONFIG['DEFORM']['PASSWORD']
            ),
            raises(ConflictError, '^User already exists.$')
        )

    def test_confirm(self):
        session_id = 'Qivjy3PW3dqxAOY9i4MeT1H0FHyGkw'
        with responses.RequestsMock() as rsps:
            rsps.add(
                self.deform_client.user.confirm.method.upper(),
                self.deform_client.user.confirm.get_context({})['url'],
                json={
                    'result': {
                        'sessionId': session_id
                    }
                },
                status=200
            )
            response = self.deform_client.user.confirm(
                code='12345'
            )
            assert_that(
                response,
                has_entry('sessionId', session_id)
            )

    def test_confirm_not_existing_code(self):
        assert_that(
            calling(self.deform_client.user.confirm).with_args(
                code='12345'
            ),
            raises(NotFoundError, '^Confirmation code not found\.$')
        )

    def test_confirm_already_confirmed_code(self):
        with responses.RequestsMock() as rsps:
            rsps.add(
                self.deform_client.user.confirm.method.upper(),
                self.deform_client.user.confirm.get_context({})['url'],
                json={
                    'result': {
                        'message': 'User already exists.'
                    }
                },
                status=409
            )
            assert_that(
                calling(self.deform_client.user.confirm).with_args(
                    code='12345'
                ),
                raises(ConflictError, '^User already exists\.$')
            )


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
