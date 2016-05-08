# -*- coding: utf-8 -*-
import hashlib
import os

from hamcrest import (
    assert_that,
    calling,
    equal_to,
    has_entries,
    has_entry,
    raises
)
from pydeform.exceptions import NotFoundError, ValidationError
from testutils import (
    DeformSessionProjectClientTestCaseMixin,
    DeformTokenProjectClientTestCaseMixin,
    TestCase
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
            calling(
                getattr(self, self.project_client_attr).document.get
            ).with_args(
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

        assert_that(
            calling(
                getattr(self, self.project_client_attr).document.get
            ).with_args(
                collection='venues',
                identity='subway',
                property=['comment', 'user', 'surname']
            ),
            raises(NotFoundError, '^Document property not found\.$')
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
            calling(
                getattr(self, self.project_client_attr).document.save
            ).with_args(
                collection='venues',
                data={
                    '_id': 'subway'
                }
            ),
            raises(ValidationError, '^Validation error$')
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

    def test_file(self):
        # remove all files
        getattr(self, self.project_client_attr).documents.remove(
            collection='_files'
        )

        getattr(self, self.project_client_attr).collection.save(
            identity='venues',
            data={
                'name': 'Venues',
                'schema': {
                    'properties': {
                        'name': {
                            'type': 'string',
                            'required': True
                        },
                        'info': {
                            'type': 'file',
                            'required': True
                        },
                        'logo': {
                            'type': 'file',
                            'required': True
                        }
                    }
                }
            }
        )
        text_file = open(
            os.path.join(self.CONFIG['FILES_PATH'], '1.txt'), 'rt'
        )
        image_file = open(
            os.path.join(self.CONFIG['FILES_PATH'], '1.png'), 'rb'
        )

        # test upload
        response = getattr(self, self.project_client_attr).document.save(
            identity='subway',
            collection='venues',
            data={
                'name': 'subway',
                'info': text_file,
                'logo': image_file,
            }
        )
        result = response['result']

        text_file.seek(0)
        image_file.seek(0)
        text_file_content = text_file.read()
        image_file_content = image_file.read()

        assert_that(
            result,
            has_entries({
                'name': 'subway',
                'info': has_entries({
                    'name': '1.txt',
                    'content_type': 'text/plain',
                    'md5': hashlib.md5(text_file_content).hexdigest()
                }),
                'logo': has_entries({
                    'name': '1.png',
                    'content_type': 'image/png',
                    'md5': hashlib.md5(image_file_content).hexdigest()
                })
            })
        )

        # test download
        info_content_response = getattr(
            self,
            self.project_client_attr
        ).document.get(
            identity='subway',
            collection='venues',
            property=['info', 'content']
        )
        assert_that(info_content_response, equal_to(text_file_content))

        logo_content_response = getattr(
            self,
            self.project_client_attr
        ).document.get(
            identity='subway',
            collection='venues',
            property=['logo', 'content']
        )
        assert_that(logo_content_response, equal_to(image_file_content))

        # test getting file object
        info_content_stream_response = getattr(
            self,
            self.project_client_attr
        ).document.get_file(
            identity='subway',
            collection='venues',
            property=['info'],
        )
        assert_that(
            info_content_stream_response.read(),
            equal_to(text_file_content)
        )

        logo_content_stream_response = getattr(
            self,
            self.project_client_attr
        ).document.get_file(
            identity='subway',
            collection='venues',
            property=['logo'],
        )
        assert_that(
            logo_content_stream_response.read(),
            equal_to(image_file_content)
        )

    def test_file_upload_directly_to_files_collection(self):
        getattr(self, self.project_client_attr).documents.remove(
            collection='_files'
        )

        text_file = open(
            os.path.join(self.CONFIG['FILES_PATH'], '1.txt'), 'rt'
        )
        image_file = open(
            os.path.join(self.CONFIG['FILES_PATH'], '1.png'), 'rb'
        )

        # test upload text file
        response = getattr(self, self.project_client_attr).document.save(
            identity='text_file',
            collection='_files',
            data=text_file
        )
        text_file_result = response['result']

        text_file.seek(0)
        text_file_content = text_file.read()

        assert_that(
            text_file_result,
            has_entries({
                '_id': 'text_file',
                'collection_id': '_files',
                'content_type': 'text/plain',
                'document_id': '',
                'name': '1.txt',
                'md5': hashlib.md5(text_file_content).hexdigest()
            })
        )

        # test upload binary file
        response = getattr(self, self.project_client_attr).document.save(
            identity='image_file',
            collection='_files',
            data=image_file
        )
        text_file_result = response['result']

        image_file.seek(0)
        image_file_content = image_file.read()

        assert_that(
            text_file_result,
            has_entries({
                '_id': 'image_file',
                'collection_id': '_files',
                'content_type': 'image/png',
                'document_id': '',
                'name': '1.png',
                'md5': hashlib.md5(image_file_content).hexdigest()
            })
        )

        # test getting text file object
        text_file_content_stream_response = getattr(
            self,
            self.project_client_attr
        ).document.get_file(
            identity='text_file',
            collection='_files'
        )
        assert_that(
            text_file_content_stream_response.read(),
            equal_to(text_file_content)
        )

        # test getting image file object
        image_file_content_stream_response = getattr(
            self,
            self.project_client_attr
        ).document.get_file(
            identity='image_file',
            collection='_files'
        )
        assert_that(
            image_file_content_stream_response.read(),
            equal_to(image_file_content)
        )


class SessionProjectClientTest__document(
    ProjectClientTestBase__document,
    DeformSessionProjectClientTestCaseMixin,
    TestCase
):
    project_client_attr = 'deform_session_project_client'


class TokenProjectClientTest__document(
    ProjectClientTestBase__document,
    DeformTokenProjectClientTestCaseMixin,
    TestCase
):
    project_client_attr = 'deform_token_project_client'
