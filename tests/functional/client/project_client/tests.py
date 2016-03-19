# -*- coding: utf-8 -*-
from hamcrest import assert_that, calling, has_entry, raises
from pydeform.exceptions import AuthError
from testutils import (
    DeformSessionProjectClientTestCaseMixin,
    DeformTokenProjectClientTestCaseMixin,
    TestCase
)


class ProjectClientTest__info(DeformSessionProjectClientTestCaseMixin,
                              DeformTokenProjectClientTestCaseMixin,
                              TestCase):
    def test_with_session_auth(self):
        response = self.deform_session_project_client.info.get()
        assert_that(
            response,
            has_entry('_id', self.CONFIG['DEFORM']['PROJECT'])
        )
        assert_that(
            response,
            has_entry('name', self.CONFIG['DEFORM']['PROJECT_NAME'])
        )

    def test_with_token_auth(self):
        assert_that(
            calling(self.deform_token_project_client.info.get),
            raises(AuthError)
        )
