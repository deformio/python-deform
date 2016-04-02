# -*- coding: utf-8 -*-
from requests import Session

from hamcrest import assert_that, equal_to, instance_of
from pydeform import Client
from testutils import TestCase


class ClientTest__init(TestCase):
    def test_defaults(self):
        client_instance = Client('deform.io')
        assert_that(client_instance.host, equal_to('deform.io'))
        assert_that(client_instance.port, equal_to(None))
        assert_that(client_instance.secure, equal_to(True))
        assert_that(client_instance.requests_session, instance_of(Session))
        assert_that(client_instance.request_defaults, equal_to(None))
        assert_that(client_instance.api_base_path, equal_to('/api/'))
        assert_that(
            client_instance.user.login.requests_session,
            equal_to(client_instance.requests_session)
        )
