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
    contains
)

from pydeform.exceptions import NotFoundError, ValidationError

from testutils import (
    TestCase,
    DeformSessionProjectClientTestCaseMixin,
    DeformTokenProjectClientTestCaseMixin,
)


class ProjectClientTestBase__document(object):
    project_client_attr = None

    def setUp(self):
        super(ProjectClientTestBase__document, self).setUp()

        try:
            getattr(self, self.project_client_attr).collection.remove(
                identity='venues'
            )
        except NotFoundError:
            pass

    def test_get(self):
        response = getattr(self, self.project_client_attr).document.get(
            identity=self.CONFIG['DEFORM']['PROJECT_TOKEN'],
            collection='_tokens'
        )
        assert_that(
            response,
            has_entries({
                'name': 'First project Token',
                '_id': self.CONFIG['DEFORM']['PROJECT_TOKEN'],
            })
        )

    def test_get_not_existing_document(self):
        assert_that(
            calling(getattr(self, self.project_client_attr).document.get).with_args(
                identity='not_existing_document',
                collection='_tokens'
            ),
            raises(NotFoundError, '^Document not found\.$')
        )

    def test_with_fields(self):
        response = getattr(self, self.project_client_attr).document.get(
            identity=self.CONFIG['DEFORM']['PROJECT_TOKEN'],
            collection='_tokens',
            fields=['name']
        )
        assert_that(
            response,
            equal_to({
                'name': 'First project Token',
                '_id': self.CONFIG['DEFORM']['PROJECT_TOKEN'],
            })
        )

    def test_with_fields_exclude(self):
        response = getattr(self, self.project_client_attr).document.get(
            identity=self.CONFIG['DEFORM']['PROJECT_TOKEN'],
            collection='_tokens',
            fields_exclude=['name']
        )
        assert_that('name' in response, equal_to(False))

    def test_create(self):
        try:
            getattr(self, self.project_client_attr).document.remove(
                collection='venues',
                identity='subway'
            )
        except NotFoundError:
            pass

        response = getattr(self, self.project_client_attr).document.create(
            collection='venues',
            data={
                '_id': 'subway',
                'name': 'Subway'
            }
        )
        assert_that(
            response,
            has_entries({
                '_id': 'subway',
                'name': 'Subway'
            })
        )

    def test_get_property(self):
        try:
            getattr(self, self.project_client_attr).document.remove(
                collection='venues',
                identity='subway'
            )
        except NotFoundError:
            pass

        response = getattr(self, self.project_client_attr).document.create(
            collection='venues',
            data={
                '_id': 'subway',
                'name': 'Subway',
                'comment': {
                    'user': {
                        'name': 'gennady',
                        'surname': 'chibisov'
                    }
                }
            }
        )

        response = getattr(self, self.project_client_attr).document.get(
            collection='venues',
            identity='subway',
            property=['comment', 'user']
        )
        assert_that(
            response,
            equal_to({
                'name': 'gennady',
                'surname': 'chibisov'
            })
        )

    def test_get_not_existing_property(self):
        try:
            getattr(self, self.project_client_attr).document.remove(
                collection='venues',
                identity='subway'
            )
        except NotFoundError:
            pass

        response = getattr(self, self.project_client_attr).document.create(
            collection='venues',
            data={
                '_id': 'subway',
                'name': 'Subway',
                'comment': {
                    'user': {
                        'name': 'gennady'
                    }
                }
            }
        )

        assert_that(
            calling(getattr(self, self.project_client_attr).document.get).with_args(
                collection='venues',
                identity='subway',
                property=['comment', 'user', 'surname']
            ),
            raises(NotFoundError, '^Property surname does not exist$')
        )

    def test_save__with_identity(self):
        try:
            getattr(self, self.project_client_attr).document.remove(
                identity='subway',
                collection='venues'
            )
        except NotFoundError:
            pass

        # first save
        response = getattr(self, self.project_client_attr).document.save(
            identity='subway',
            collection='venues',
            data={
                'name': 'Subway'
            }
        )
        assert_that(response['created'], equal_to(True))
        assert_that(
            response['result'],
            has_entries({
                '_id': 'subway',
                'name': 'Subway'
            })
        )

        # second save
        response = getattr(self, self.project_client_attr).document.save(
            identity='subway',
            collection='venues',
            data={
                'name': 'Subway saved with identity'
            }
        )
        assert_that(response['created'], equal_to(False))
        assert_that(
            response['result'],
            has_entries({
                '_id': 'subway',
                'name': 'Subway saved with identity',
            })
        )

    def test_save__without_identity(self):
        try:
            getattr(self, self.project_client_attr).document.remove(
                identity='subway',
                collection='venues'
            )
        except NotFoundError:
            pass

        # first save
        response = getattr(self, self.project_client_attr).document.save(
            collection='venues',
            data={
                '_id': 'subway',
                'name': 'Subway'
            }
        )
        assert_that(response['created'], equal_to(True))
        assert_that(
            response['result'],
            has_entries({
                '_id': 'subway',
                'name': 'Subway'
            })
        )

        # second save
        response = getattr(self, self.project_client_attr).document.save(
            collection='venues',
            data={
                '_id': 'subway',
                'name': 'Subway saved with identity'
            }
        )
        assert_that(response['created'], equal_to(False))
        assert_that(
            response['result'],
            has_entries({
                '_id': 'subway',
                'name': 'Subway saved with identity',
            })
        )

    def test_save_property(self):
        try:
            getattr(self, self.project_client_attr).document.remove(
                identity='subway',
                collection='venues'
            )
        except NotFoundError:
            pass

        getattr(self, self.project_client_attr).document.create(
            collection='venues',
            data={
                '_id': 'subway',
                'name': 'Subway',
                'comment': {
                    'user': {
                        'name': 'gennady'
                    }
                }
            }
        )

        response = getattr(self, self.project_client_attr).document.save(
            identity='subway',
            collection='venues',
            property=['comment', 'user', 'surname'],
            data='chibisov'
        )
        assert_that(response['created'], equal_to(True))
        assert_that(response['result'], equal_to('chibisov'))

        response = getattr(self, self.project_client_attr).document.get(
            identity='subway',
            collection='venues',
            property=['comment', 'user']
        )
        assert_that(
            response,
            has_entries({
                'name': 'gennady',
                'surname': 'chibisov',
            })
        )

        # should replace property
        response = getattr(self, self.project_client_attr).document.save(
            identity='subway',
            collection='venues',
            property=['comment', 'user'],
            data={
                'name': 'andrey'
            }
        )
        assert_that(response['created'], equal_to(False))
        assert_that(response['result'], equal_to({'name': 'andrey'}))

        response = getattr(self, self.project_client_attr).document.get(
            identity='subway',
            collection='venues',
            property=['comment', 'user']
        )
        assert_that(
            response,
            equal_to({
                'name': 'andrey'
            })
        )

    def test_update(self):
        try:
            getattr(self, self.project_client_attr).document.remove(
                identity='subway',
                collection='venues'
            )
        except NotFoundError:
            pass

        getattr(self, self.project_client_attr).document.create(
            collection='venues',
            data={
                '_id': 'subway',
                'name': 'Subway',
                'comment': {
                    'user': 'gena',
                    'text': 'good'
                }
            }
        )

        response = getattr(self, self.project_client_attr).document.update(
            identity='subway',
            collection='venues',
            data={
                'comment': {
                    'text': 'bad'
                }
            }
        )
        assert_that(
            response['comment'],
            equal_to({
                'text': 'bad'
            })
        )

    def test_remove(self):
        getattr(self, self.project_client_attr).document.save(
            collection='venues',
            data={
                '_id': 'subway',
                'name': 'Subway'
            }
        )
        response = getattr(self, self.project_client_attr).document.remove(
            identity='subway',
            collection='venues'
        )
        assert_that(response, equal_to(None))

    def test_schema_validation(self):
        getattr(self, self.project_client_attr).collection.save(
            identity='venues',
            data={
                'name': 'Venues',
                'schema': {
                    'properties': {
                        'name': {
                            'type': 'string',
                            'required': True
                        }
                    }
                }
            }
        )

        assert_that(
            calling(getattr(self, self.project_client_attr).document.save).with_args(
                collection='venues',
                data={
                    '_id': 'subway'
                }
            ),
            raises(ValidationError, '^name is required$')
        )

        response = getattr(self, self.project_client_attr).document.save(
            collection='venues',
            data={
                '_id': 'subway',
                'name': 'Subway'
            }
        )
        assert_that(
            response['result'],
            has_entry('name', 'Subway')
        )



class SessionProjectClientTest__document(ProjectClientTestBase__document,
                                         DeformSessionProjectClientTestCaseMixin,
                                         TestCase):
    project_client_attr = 'deform_session_project_client'


class TokenProjectClientTest__document(ProjectClientTestBase__document,
                                       DeformTokenProjectClientTestCaseMixin,
                                       TestCase):
    project_client_attr = 'deform_token_project_client'
