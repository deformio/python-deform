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


class ProjectClientTestBase__collection(object):
    project_client_attr = None

    def test_get(self):
        response = getattr(self, self.project_client_attr).collection.get(identity='_users')
        assert_that(
            response,
            has_entries({
                'name': 'Users',
                '_id': '_users',
                'is_system': True,
            })
        )

    def test_create(self):
        try:
            getattr(self, self.project_client_attr).collection.remove(identity='venues')
        except NotFoundError:
            pass

        response = getattr(self, self.project_client_attr).collection.create(
            data={
                '_id': 'venues',
                'name': 'Venues'
            }
        )
        assert_that(
            response,
            has_entries({
                'name': 'Venues',
                '_id': 'venues',
                'is_system': False,
            })
        )

    def test_save__with_identity(self):
        try:
            getattr(self, self.project_client_attr).collection.remove(identity='venues')
        except NotFoundError:
            pass

        # first save
        response = getattr(self, self.project_client_attr).collection.save(
            identity='venues',
            data={
                'name': 'Venues'
            }
        )
        assert_that(response['created'], equal_to(True))
        assert_that(
            response['result'],
            has_entries({
                'name': 'Venues',
                '_id': 'venues',
                'is_system': False,
            })
        )

        # second save
        response = getattr(self, self.project_client_attr).collection.save(
            identity='venues',
            data={
                'name': 'Venues saved with identity'
            }
        )
        assert_that(response['created'], equal_to(False))
        assert_that(
            response['result'],
            has_entries({
                'name': 'Venues saved with identity',
                '_id': 'venues',
                'is_system': False,
            })
        )

    def test_save__without_identity(self):
        try:
            getattr(self, self.project_client_attr).collection.remove(identity='venues')
        except NotFoundError:
            pass

        # first save
        response = getattr(self, self.project_client_attr).collection.save(
            data={
                '_id': 'venues',
                'name': 'Venues'
            }
        )
        assert_that(response['created'], equal_to(True))
        assert_that(
            response['result'],
            has_entries({
                'name': 'Venues',
                '_id': 'venues',
                'is_system': False,
            })
        )

        # second save
        response = getattr(self, self.project_client_attr).collection.save(
            data={
                '_id': 'venues',
                'name': 'Venues saved with identity'
            }
        )
        assert_that(response['created'], equal_to(False))
        assert_that(
            response['result'],
            has_entries({
                'name': 'Venues saved with identity',
                '_id': 'venues',
                'is_system': False,
            })
        )

    def test_update(self):
        try:
            getattr(self, self.project_client_attr).collection.remove(identity='venues')
        except NotFoundError:
            pass

        response = getattr(self, self.project_client_attr).collection.create(
            data={
                '_id': 'venues',
                'name': 'Venues'
            }
        )
        assert_that(
            response['schema'],
            has_entry(
                'additionalProperties',
                True
            )
        )

        response = getattr(self, self.project_client_attr).collection.update(
            identity='venues',
            data={
                'schema': {
                    'additionalProperties': False,
                }
            }
        )
        assert_that(
            response['schema'],
            has_entry(
                'additionalProperties',
                False
            )
        )

    def test_remove(self):
        getattr(self, self.project_client_attr).collection.save(
            data={
                '_id': 'venues',
                'name': 'Venues'
            }
        )
        response = getattr(self, self.project_client_attr).collection.remove(identity='venues')
        assert_that(response, equal_to(None))


class SessionProjectClientTest__collection(DeformSessionProjectClientTestCaseMixin,
                                           ProjectClientTestBase__collection,
                                           TestCase):
    project_client_attr = 'deform_session_project_client'


class TokenProjectClientTest__collection(DeformTokenProjectClientTestCaseMixin,
                                         ProjectClientTestBase__collection,
                                         TestCase):
    project_client_attr = 'deform_token_project_client'
