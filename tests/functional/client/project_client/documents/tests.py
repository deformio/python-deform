# -*- coding: utf-8 -*-
from hamcrest import (
    assert_that,
    calling,
    contains_inanyorder,
    equal_to,
    is_not,
    raises
)
from pydeform.exceptions import NotFoundError
from testutils import (
    DeformSessionProjectClientTestCaseMixin,
    DeformTokenProjectClientTestCaseMixin,
    TestCase
)


class ProjectClientTestBase__documents(object):
    project_client_attr = None

    def setUp(self):
        super(ProjectClientTestBase__documents, self).setUp()

        try:
            getattr(self, self.project_client_attr).documents.remove(
                collection='venues'
            )
        except NotFoundError:
            pass

        self.documents = {
            'subway': getattr(self, self.project_client_attr).document.save(
                collection='venues',
                data={
                    '_id': 'subway',
                    'name': 'Subway',
                    'address': 'Moscow'
                }
            )['result'],
            'mcdonalds': getattr(self, self.project_client_attr).document.save(
                collection='venues',
                data={
                    '_id': 'mcdonalds',
                    'name': 'McDonalds',
                    'address': 'London'
                }
            )['result']
        }

    def convert_generator_to_list(self, generator):
        return [i for i in generator]

    def test_find_is_paginatable(self):
        assert_that(
            getattr(
                self,
                self.project_client_attr
            ).documents.find.is_paginatable,
            equal_to(True)
        )

    def test_find__with_not_existing_collection(self):
        try:
            getattr(self, self.project_client_attr).collection.remove(
                identity='venues'
            )
        except NotFoundError:
            pass

        try:
            [i for i in getattr(self, self.project_client_attr).documents.find(collection='venues')]
        except NotFoundError as e:
            assert_that(str(e), equal_to('Collection not found.'))
        else:
            raise Exception(
                'NotFoundError should be raised for not existing collection'
            )

    def test_find(self):
        response = getattr(self, self.project_client_attr).documents.find(
            collection='venues'
        )
        response = self.convert_generator_to_list(response)
        assert_that(
            response,
            contains_inanyorder(*self.documents.values())
        )

    def test_find__filter(self):
        response = getattr(self, self.project_client_attr).documents.find(
            collection='venues',
            filter={
                'name': 'Subway'
            }
        )
        response = self.convert_generator_to_list(response)
        assert_that(len(response), equal_to(1))
        assert_that(response[0], self.documents['subway'])

    def test_find__text(self):
        response = getattr(self, self.project_client_attr).collection.update(
            identity='venues',
            data={
                'indexes': [
                    {
                        'property': 'name',
                        'type': 'text',
                        'language': 'en'
                    }
                ]
            }
        )
        response = getattr(self, self.project_client_attr).documents.find(
            collection='venues',
            text='Subway'
        )
        response = self.convert_generator_to_list(response)
        assert_that(len(response), equal_to(1))
        assert_that(response[0], equal_to(self.documents['subway']))

    def test_find__with_fields(self):
        response = getattr(self, self.project_client_attr).documents.find(
            collection='venues',
            fields=['name']
        )
        response = self.convert_generator_to_list(response)
        expected = [
            {'_id': i['_id'], 'name': i['name']}
            for i in self.documents.values()
        ]
        assert_that(
            response,
            contains_inanyorder(*expected)
        )

    def test_find__with_fields_exclude(self):
        response = getattr(self, self.project_client_attr).documents.find(
            collection='venues',
            fields_exclude=['name']
        )
        response = self.convert_generator_to_list(response)
        expected = [
            {'_id': i['_id'], 'address': i['address']}
            for i in self.documents.values()
        ]
        assert_that(
            response,
            contains_inanyorder(*expected)
        )

    def test_find_sort(self):
        response_1 = getattr(self, self.project_client_attr).documents.find(
            collection='venues',
            sort=['_id']
        )
        response_1 = self.convert_generator_to_list(response_1)
        response_2 = getattr(self, self.project_client_attr).documents.find(
            collection='venues',
            sort=['-_id']
        )
        response_2 = self.convert_generator_to_list(response_2)
        for i, item in enumerate(response_1):
            j = (i + 1) * -1
            assert_that(
                item,
                equal_to(response_2[j]),
                'item %s and %s does not equal' % (i, j)
            )

    def test_count(self):
        response = getattr(self, self.project_client_attr).documents.count(
            collection='venues'
        )
        assert_that(response, equal_to(2))

    def test_count__filter(self):
        response = getattr(self, self.project_client_attr).documents.count(
            collection='venues',
            filter={
                'name': 'Subway'
            }
        )
        assert_that(response, equal_to(1))

    def test_count__text(self):
        response = getattr(self, self.project_client_attr).collection.update(
            identity='venues',
            data={
                'indexes': [
                    {
                        'property': 'name',
                        'type': 'text',
                        'language': 'en'
                    }
                ]
            }
        )
        response = getattr(self, self.project_client_attr).documents.count(
            collection='venues',
            text='Subway'
        )
        assert_that(response, equal_to(1))

    def test_update_all(self):
        response = getattr(self, self.project_client_attr).documents.update(
            collection='venues',
            operation={
                '$inc': {
                    'rating': 1
                }
            }
        )
        assert_that(response['updated'], equal_to(2))
        response = getattr(self, self.project_client_attr).documents.find(
            collection='venues'
        )
        response = self.convert_generator_to_list(response)
        self.documents['mcdonalds']['rating'] = 1
        self.documents['subway']['rating'] = 1
        assert_that(
            response,
            contains_inanyorder(*self.documents.values())
        )

    def test_update_by_filter(self):
        response = getattr(self, self.project_client_attr).documents.update(
            collection='venues',
            filter={
                'name': 'Subway'
            },
            operation={
                '$inc': {
                    'rating': 1
                }
            }
        )
        assert_that(response['updated'], equal_to(1))
        response = getattr(self, self.project_client_attr).documents.find(
            collection='venues'
        )
        response = self.convert_generator_to_list(response)
        self.documents['subway']['rating'] = 1
        assert_that(
            response,
            contains_inanyorder(*self.documents.values())
        )

    def test_upsert_with_existing_document(self):
        response = getattr(self, self.project_client_attr).documents.upsert(
            collection='venues',
            filter={
                'name': 'Subway'
            },
            operation={
                '$inc': {
                    'rating': 1
                }
            }
        )
        assert_that(response['updated'], equal_to(1))
        assert_that('upsertedId' in response, equal_to(False))
        response = getattr(self, self.project_client_attr).documents.find(
            collection='venues'
        )
        response = self.convert_generator_to_list(response)
        self.documents['subway']['rating'] = 1
        assert_that(
            response,
            contains_inanyorder(*self.documents.values())
        )

    def test_upsert_without_document(self):
        response = getattr(self, self.project_client_attr).documents.upsert(
            collection='venues',
            filter={
                'name': 'KFC'
            },
            operation={
                '$inc': {
                    'rating': 1
                }
            }
        )
        assert_that('updated' in response, equal_to(False))
        assert_that(response.get('upsertedId'), is_not(equal_to(None)))
        upserted_id = response['upsertedId']
        response = getattr(self, self.project_client_attr).documents.find(
            collection='venues'
        )
        response = self.convert_generator_to_list(response)
        self.documents['kfc'] = {
            '_id': upserted_id,
            'name': 'KFC',
            'rating': 1
        }
        assert_that(
            response,
            contains_inanyorder(*self.documents.values())
        )

    def test_remove_all(self):
        response = getattr(self, self.project_client_attr).documents.remove(
            collection='venues'
        )
        assert_that(response['deleted'], equal_to(2))
        response = getattr(self, self.project_client_attr).documents.find(
            collection='venues'
        )
        response = self.convert_generator_to_list(response)
        assert_that(response, equal_to([]))

    def test_remove_by_filter(self):
        response = getattr(self, self.project_client_attr).documents.remove(
            collection='venues',
            filter={
                'name': 'Subway'
            }
        )
        assert_that(response['deleted'], equal_to(1))
        response = getattr(self, self.project_client_attr).documents.find(
            collection='venues'
        )
        response = self.convert_generator_to_list(response)
        assert_that(len(response), equal_to(1))
        assert_that(response[0], equal_to(self.documents['mcdonalds']))


class SessionProjectClientTest__documents(
    ProjectClientTestBase__documents,
    DeformSessionProjectClientTestCaseMixin,
    TestCase
):
    project_client_attr = 'deform_session_project_client'


class TokenProjectClientTest__documents(
    ProjectClientTestBase__documents,
    DeformTokenProjectClientTestCaseMixin,
    TestCase
):
    project_client_attr = 'deform_token_project_client'
