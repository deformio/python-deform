# -*- coding: utf-8 -*-
from pydeform.resources.base import (
    BaseResource,
    ResourceMethodBase,
    GetListResourceMethod,
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
    method = 'post'
    params = {
        'email': PARAMS_DEFINITIONS['login_email'],
        'password': PARAMS_DEFINITIONS['login_password'],
    }
    params_required = ['email', 'password']


class NonAuthUserResourceLoginMethod(ResourceMethodBase):
    action = 'login'
    params = {
        'email': PARAMS_DEFINITIONS['login_email'],
        'password': PARAMS_DEFINITIONS['login_password'],
    }
    params_required = ['email', 'password']
    result_property = 'sessionId'


class NonAuthUserResourceConfirmMethod(ResourceMethodBase):
    action = 'confirm'
    params = {
        'code': PARAMS_DEFINITIONS['confirm_code'],
    }
    params_required = ['code']


class NonAuthUserResource(BaseResource):
    path = ['user']

    methods = {
        'create': NonAuthUserResourceCreateMethod,
        'confirm': NonAuthUserResourceConfirmMethod,
        'login': NonAuthUserResourceLoginMethod,
    }


class SessionUserResource(BaseResource):
    path = ['user']

    methods = {
        'get': GetResourceMethod,
        'logout': type('SessionUserResourceLogout', (ResourceMethodBase,), {'action': 'logout'}),
        'update': UpdateResourceMethod
    }


class ProjectListResource(BaseResource):
    path = ['user', 'projects']

    methods = {
        'find': FindListResourceMethod,
        'count': CountListResourceMethod,
    }


class ProjectOneResource(BaseResource):
    path = ['user', 'projects', '{identity}']

    methods = {
        'get': GetOneResourceMethod,
        'save': SaveOneResourceMethod,
        'create': CreateOneResourceMethod,
    }


class CurrentProjectInfoResource(BaseResource):
    path = ['info']

    methods = {
        'get': GetResourceMethod,
    }


class CollectionListResource(BaseResource):
    path = ['collections']

    methods = {
        'find': FindListResourceMethod,
        'count': CountListResourceMethod,
    }


class CollectionOneResource(BaseResource):
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
        params_required = super(DocumentResourceMixin, self).get_params_required()
        params_required.append('collection')
        return params_required


class DocumentListResource(BaseResource):
    path = ['collections', '{collection}', 'documents']

    methods = {
        'find': type('DocumentFindListResourceMethod', (DocumentResourceMixin, FindListResourceMethod), {}),
        'count': type('DocumentFindListResourceMethod', (DocumentResourceMixin, CountListResourceMethod), {}),
        'update': type('DocumentUpdateListResourceMethod', (DocumentResourceMixin, UpdateListResourceMethod), {}),
        'upsert': type('DocumentUpsertListResourceMethod', (DocumentResourceMixin, UpsertListResourceMethod), {}),
        'remove': type('DocumentRemoveListResourceMethod', (DocumentResourceMixin, RemoveListResourceMethod), {}),
    }


class DocumentOneResource(BaseResource):
    path = ['collections', '{collection}', 'documents', '{identity}', '{property}']

    methods = {
        'get': type('DocumentGetOneResourceMethod', (DocumentResourceMixin, GetOneResourceMethod), {}),
        'get_file': type('DocumentGetOneResourceMethod', (DocumentResourceMixin, GetFileResourceMethod), {}),
        'create': type('DocumentCreateOneResourceMethod', (DocumentResourceMixin, CreateOneResourceMethod), {}),
        'save': type('DocumentSaveOneResourceMethod', (DocumentResourceMixin, SaveOneResourceMethod), {}),
        'update': type('DocumentUpdateOneResourceMethod', (DocumentResourceMixin, UpdateOneResourceMethod), {}),
        'remove': type('DocumentRemoveOneResourceMethod', (DocumentResourceMixin, RemoveOneResourceMethod), {}),
    }
