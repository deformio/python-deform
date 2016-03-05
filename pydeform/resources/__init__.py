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
        'all': GetListResourceMethod,
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
        'all': GetListResourceMethod,
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


class DocumentResourceMixin(object):
    def get_params_definitions(self):
        params = super(DocumentResourceMixin, self).get_params_definitions()
        params['collection'] = PARAMS_DEFINITIONS['collection']
        return params

    def get_params_required(self):
        params_required = super(DocumentResourceMixin, self).get_params_required_definitions()
        params_required.append('collection')
        return params_required


class DocumentListResource(BaseResource):
    path = ['documents']

    methods = {
        'all': type('DocumentGetListResourceMethod', (DocumentResourceMixin, GetListResourceMethod), {}),
        'find': type('DocumentFindListResourceMethod', (DocumentResourceMixin, FindListResourceMethod), {}),
        'update': type('DocumentUpdateListResourceMethod', (DocumentResourceMixin, UpdateListResourceMethod), {}),
        'upsert': type('DocumentUpsertListResourceMethod', (DocumentResourceMixin, UpsertListResourceMethod), {}),
        'remove': type('DocumentRemoveListResourceMethod', (DocumentResourceMixin, RemoveListResourceMethod), {}),
    }


class DocumentOneResource(BaseResource):
    path = ['documents']

    methods = {
        'get': type('DocumentGetOneResourceMethod', (DocumentResourceMixin, GetOneResourceMethod), {}),
        'create': type('DocumentCreateOneResourceMethod', (DocumentResourceMixin, CreateOneResourceMethod), {}),
        'save': type('DocumentSaveOneResourceMethod', (DocumentResourceMixin, SaveOneResourceMethod), {}),
        'update': type('DocumentUpdateOneResourceMethod', (DocumentResourceMixin, UpdateOneResourceMethod), {}),
        'remove': type('DocumentRemoveOneResourceMethod', (DocumentResourceMixin, RemoveOneResourceMethod), {}),
    }
