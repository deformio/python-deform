# -*- coding: utf-8 -*-
from pydeform.resources.base import (
    BaseResource,
    GetListResourceMethod,
    FindListResourceMethod,
    UpdateListResourceMethod,
    UpsertListResourceMethod,
    RemoveListResourceMethod,
    GetResourceMethod,
    GetOneResourceMethod,
    CreateOneResourceMethod,
    SaveOneResourceMethod,
    UpdateOneResourceMethod,
    RemoveOneResourceMethod,
)
from pydeform.resources.utils import PARAMS_DEFINITIONS


class UserOneResource(BaseResource):
    path = ['user']

    methods = {
        'get': GetResourceMethod,
    }


class ProjectListResource(BaseResource):
    path = ['user', 'projects']

    methods = {
        'find': FindListResourceMethod,
    }


class ProjectOneResource(BaseResource):
    path = ['user', 'projects']

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
    }


class CollectionOneResource(BaseResource):
    path = ['collections']

    methods = {
        'get': GetOneResourceMethod,
        'create': CreateOneResourceMethod,
        'save': SaveOneResourceMethod,
        'update': UpdateOneResourceMethod,
        'remove': RemoveOneResourceMethod,
    }


class DocumentListResourceMixin(object):
    def get_params_definitions(self):
        params = super(DocumentListResourceMixin, self).get_params_definitions()
        params['fields'] = PARAMS_DEFINITIONS['fields']
        params['fields_exclude'] = PARAMS_DEFINITIONS['fields_exclude']
        return params


class DocumentOneResourceMixin(object):
    def get_params_definitions(self):
        params = super(DocumentOneResourceMixin, self).get_params_definitions()
        params['collection'] = PARAMS_DEFINITIONS['collection']
        return params

    def get_params_required(self):
        params_required = super(DocumentOneResourceMixin, self).get_params_required_definitions()
        params_required.append('collection')
        return params_required


class DocumentListResource(BaseResource):
    path = ['documents']

    methods = {
        'find': type('DocumentFindListResourceMethod', (DocumentListResourceMixin, FindListResourceMethod), {}),
        'update': type('DocumentUpdateListResourceMethod', (DocumentListResourceMixin, UpdateListResourceMethod), {}),
        'upsert': type('DocumentUpsertListResourceMethod', (DocumentListResourceMixin, UpsertListResourceMethod), {}),
        'remove': type('DocumentRemoveListResourceMethod', (DocumentListResourceMixin, RemoveListResourceMethod), {}),
    }


class DocumentOneResource(BaseResource):
    path = ['documents']

    methods = {
        'get': type('DocumentGetOneResourceMethod', (DocumentOneResourceMixin, GetOneResourceMethod), {}),
        'create': type('DocumentCreateOneResourceMethod', (DocumentOneResourceMixin, CreateOneResourceMethod), {}),
        'save': type('DocumentSaveOneResourceMethod', (DocumentOneResourceMixin, SaveOneResourceMethod), {}),
        'update': type('DocumentUpdateOneResourceMethod', (DocumentOneResourceMixin, UpdateOneResourceMethod), {}),
        'remove': type('DocumentRemoveOneResourceMethod', (DocumentOneResourceMixin, RemoveOneResourceMethod), {}),
    }
