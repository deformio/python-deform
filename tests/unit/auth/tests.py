# -*- coding: utf-8 -*-
from hamcrest import (
    assert_that,
    not_none,
    equal_to,
    instance_of,
    calling,
    raises
)

from pydeform.auth import (
    get_session_id,
    get_session_http_auth_header,
    get_token_http_auth_header,
)
from pydeform.utils import get_base_uri
from pydeform.exceptions import AuthError
from pydeform import six

from testutils import (
    DeformBaseURITestCaseMixin,
    TestCase,
    check_timeout
)


class Test__get_session_id(DeformBaseURITestCaseMixin, TestCase):
    def test_wrong_credentials(self):
        assert_that(
            calling(get_session_id).with_args(
                base_uri=self.DEFORM_BASE_URI,
                email='wrong-' + self.CONFIG['DEFORM']['EMAIL'],
                password='wrong-' + self.CONFIG['DEFORM']['PASSWORD'],
                requests_session=self.requests_session,
                request_defaults=self.request_defaults
            ),
            raises(AuthError, '^Wrong credentials provided.$')
        )

    def test_timeout(self):
        check_timeout(
            get_session_id,
            kwargs=dict(
                base_uri=self.DEFORM_BASE_URI,
                email='wrong-' + self.CONFIG['DEFORM']['EMAIL'],
                password='wrong-' + self.CONFIG['DEFORM']['PASSWORD'],
                requests_session=self.requests_session,
                request_defaults=self.request_defaults
            )
        )

    def test_right_credentials(self):
        response = get_session_id(
            base_uri=self.DEFORM_BASE_URI,
            email=self.CONFIG['DEFORM']['EMAIL'],
            password=self.CONFIG['DEFORM']['PASSWORD'],
            requests_session=self.requests_session,
            request_defaults=self.request_defaults
        )
        assert_that(response, not_none)
        assert_that(response, instance_of(six.text_type))


class Test__get_session_http_auth_header(TestCase):
    def test_me(self):
        assert_that(get_session_http_auth_header('hello'), 'SessionId hello')


class Test__get_token_http_auth_header(TestCase):
    def test_me(self):
        assert_that(get_token_http_auth_header('hello'), 'Token hello')
