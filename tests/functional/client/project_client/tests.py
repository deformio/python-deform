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
    has_entries,
    is_not,
    empty
)
import responses

from pydeform import six
from pydeform.client import (
    ProjectClient,
)
from pydeform.utils import get_base_uri
from pydeform.exceptions import AuthError

from testutils import (
    DeformClientTestCaseMixin,
    TestCase,
    DeformSessionProjectClientTestCaseMixin,
    DeformTokenProjectClientTestCaseMixin,
    check_timeout
)


class ProjectClientTest__info(DeformSessionProjectClientTestCaseMixin,
                              DeformTokenProjectClientTestCaseMixin,
                              TestCase):
    def test_with_session_auth(self):
        response = self.deform_session_project_client.info.get()
        assert_that(response, has_entry('_id', self.CONFIG['DEFORM']['PROJECT']))
        assert_that(response, has_entry('name', self.CONFIG['DEFORM']['PROJECT_NAME']))

    def test_with_token_auth(self):
        assert_that(
            calling(self.deform_token_project_client.info.get),
            raises(AuthError)
        )
