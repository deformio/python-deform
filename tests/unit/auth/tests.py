# -*- coding: utf-8 -*-
from hamcrest import assert_that, equal_to
from pydeform.auth import (
    get_session_http_auth_header,
    get_token_http_auth_header
)
from testutils import TestCase


class Test__get_session_http_auth_header(TestCase):
    def test_me(self):
        assert_that(
            get_session_http_auth_header('hello'),
            equal_to('SessionId hello')
        )


class Test__get_token_http_auth_header(TestCase):
    def test_me(self):
        assert_that(
            get_token_http_auth_header('hello'),
            equal_to('Token hello')
        )
