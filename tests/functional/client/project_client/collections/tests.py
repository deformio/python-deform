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

from pydeform.exceptions import NotFoundError

from testutils import (
    TestCase,
    DeformSessionProjectClientTestCaseMixin,
    DeformTokenProjectClientTestCaseMixin,
)


class ProjectClientTestBase__collections(object):
    project_client_attr = None

    def convert_generator_to_list(self, generator):
        return [i for i in generator]

    def test_find(self):
        response = getattr(self, self.project_client_attr).collections.find()
        response = self.convert_generator_to_list(response)
        users_collection = [i for i in response if i['_id'] == '_users']
        assert_that(response, is_not(equal_to([])))

    def test_find__filter(self):
        response = getattr(self, self.project_client_attr).collections.find(
            filter={
                'name': 'Users'
            }
        )
        response = self.convert_generator_to_list(response)
        assert_that(len(response), equal_to(1))
        assert_that(response[0], has_entry('_id', '_users'))

    def test_find__text(self):
        response = getattr(self, self.project_client_attr).collections.find(
            text='Users'
        )
        response = self.convert_generator_to_list(response)
        assert_that(len(response), equal_to(1))
        assert_that(response[0], has_entry('_id', '_users'))


class SessionProjectClientTest__collections(DeformSessionProjectClientTestCaseMixin,
                                            ProjectClientTestBase__collections,
                                            TestCase):
    project_client_attr = 'deform_session_project_client'


class TokenProjectClientTest__collections(DeformTokenProjectClientTestCaseMixin,
                                          ProjectClientTestBase__collections,
                                          TestCase):
    project_client_attr = 'deform_token_project_client'
