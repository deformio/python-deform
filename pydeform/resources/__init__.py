# -*- coding: utf-8 -*-
from pydeform.resources.base import (
    BaseResource,
    ResourceMethodBase,
    FindListResourceMethod,
    CountListResourceMethod,
    UpdateListResourceMethod,
    UpsertListResourceMethod,
    RemoveListResourceMethod,
    GetResourceMethod,
    GetFileResourceMethod,
    UpdateResourceMethod,
    GetOneResourceMethod,
    CreateOneResourceMethod,
    SaveOneResourceMethod,
    UpdateOneResourceMethod,
    RemoveOneResourceMethod,
)
from pydeform.resources.utils import PARAMS_DEFINITIONS


class NonAuthUserResourceCreateMethod(ResourceMethodBase):
    """Creates user."""
    method = 'post'
    params = {
        'email': PARAMS_DEFINITIONS['login_email'],
        'password': PARAMS_DEFINITIONS['login_password'],
    }
    params_required = ['email', 'password']


class NonAuthUserResourceLoginMethod(ResourceMethodBase):
    """Login with email and password.

    Returns:
        Session id
    """
    action = 'login'
    params = {
        'email': PARAMS_DEFINITIONS['login_email'],
        'password': PARAMS_DEFINITIONS['login_password'],
    }
    params_required = ['email', 'password']
    result_property = 'sessionId'


class NonAuthUserResourceConfirmMethod(ResourceMethodBase):
    """Email confirmation method.

    Returns:
        Session id
    """
    action = 'confirm'
    params = {
        'code': PARAMS_DEFINITIONS['confirm_code'],
    }
    params_required = ['code']


class NonAuthUserResource(BaseResource):
    """Non-auth user manipulation object."""
    path = ['user']

    methods = {
        'create': NonAuthUserResourceCreateMethod,
        'confirm': NonAuthUserResourceConfirmMethod,
        'login': NonAuthUserResourceLoginMethod,
    }


class SessionUserResource(BaseResource):
    """Authenticated by session user manipulation object"""
    path = ['user']

    methods = {
        'get': GetResourceMethod,
        'logout': type(
            'SessionUserResourceLogout',
            (ResourceMethodBase,),
            {'action': 'logout'}
        ),
        'update': UpdateResourceMethod
    }


class ProjectListResource(BaseResource):
    """Many projects manipulation object"""
    path = ['user', 'projects']

    methods = {
        'find': FindListResourceMethod,
        'count': CountListResourceMethod,
    }


class ProjectOneResource(BaseResource):
    """One project manipulation object"""
    path = ['user', 'projects', '{identity}']

    methods = {
        'get': GetOneResourceMethod,
        'save': SaveOneResourceMethod,
        'create': CreateOneResourceMethod,
    }


class CurrentProjectInfoResource(BaseResource):
    """Current project manupulation object"""
    path = ['info']

    methods = {
        'get': GetResourceMethod,
    }


class CollectionListResource(BaseResource):
    """Many collections manupulation object"""
    path = ['collections']

    methods = {
        'find': FindListResourceMethod,
        'count': CountListResourceMethod,
    }


class CollectionOneResource(BaseResource):
    """One collection manupulation object"""
    path = ['collections', '{identity}', '{property}']

    methods = {
        'get': GetOneResourceMethod,
        'create': CreateOneResourceMethod,
        'save': SaveOneResourceMethod,
        'update': UpdateOneResourceMethod,
        'remove': RemoveOneResourceMethod,
    }


class DocumentResourceMixin(object):
    def get_params_definitions(self):
        params = super(DocumentResourceMixin, self).get_params_definitions()
        params['fields'] = PARAMS_DEFINITIONS['fields']
        params['fields_exclude'] = PARAMS_DEFINITIONS['fields_exclude']
        params['collection'] = PARAMS_DEFINITIONS['collection']
        return params

    def get_params_required(self):
        params_required = super(
            DocumentResourceMixin, self
        ).get_params_required()
        params_required.append('collection')
        return params_required


class DocumentRemoveOneResourceMethod(DocumentResourceMixin,
                                      RemoveOneResourceMethod):
    def get_params_definitions(self):
        params = super(
            DocumentRemoveOneResourceMethod,
            self
        ).get_params_definitions()
        params.pop('property')
        return params


class DocumentListResource(BaseResource):
    """Many documents manupulation object"""
    path = ['collections', '{collection}', 'documents']

    methods = {
        'find': type(
            'DocumentFindListResourceMethod',
            (DocumentResourceMixin, FindListResourceMethod),
            {}
        ),
        'count': type(
            'DocumentFindListResourceMethod',
            (DocumentResourceMixin, CountListResourceMethod),
            {}
        ),
        'update': type(
            'DocumentUpdateListResourceMethod',
            (DocumentResourceMixin, UpdateListResourceMethod),
            {}
        ),
        'upsert': type(
            'DocumentUpsertListResourceMethod',
            (DocumentResourceMixin, UpsertListResourceMethod),
            {}
        ),
        'remove': type(
            'DocumentRemoveListResourceMethod',
            (DocumentResourceMixin, RemoveListResourceMethod),
            {}
        ),
    }


class DocumentOneResource(BaseResource):
    """One document manupulation object"""
    path = [
        'collections',
        '{collection}',
        'documents',
        '{identity}',
        '{property}'
    ]

    methods = {
        'get': type(
            'DocumentGetOneResourceMethod',
            (DocumentResourceMixin, GetOneResourceMethod),
            {}
        ),
        'get_file': type(
            'DocumentGetOneResourceMethod',
            (DocumentResourceMixin, GetFileResourceMethod),
            {}
        ),
        'create': type(
            'DocumentCreateOneResourceMethod',
            (DocumentResourceMixin, CreateOneResourceMethod),
            {}
        ),
        'save': type(
            'DocumentSaveOneResourceMethod',
            (DocumentResourceMixin, SaveOneResourceMethod),
            {}
        ),
        'update': type(
            'DocumentUpdateOneResourceMethod',
            (DocumentResourceMixin, UpdateOneResourceMethod),
            {}
        ),
        'remove': DocumentRemoveOneResourceMethod
    }
