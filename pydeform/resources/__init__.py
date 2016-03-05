# -*- coding: utf-8 -*-
from pydeform.resources.base import (
    BaseResource,
    GetListResourceMethod,
    SearchListResourceMethod,
    UpdateListResourceMethod,
    UpsertListResourceMethod,
    RemoveListResourceMethod,
    GetOneResourceMethod,
    CreateOneResourceMethod,
    SaveOneResourceMethod,
    UpdateOneResourceMethod,
    RemoveOneResourceMethod,
)


class ProjectListResource(BaseResource):
    path = 'user/projects/'

    methods = {
        'get': GetListResourceMethod,
    }


class ProjectOneResource(BaseResource):
    path = 'user/'

    methods = {
        'get': GetOneResourceMethod,
    }


class UserOneResource(BaseResource):
    path = 'user/'

    methods = {
        'get': GetOneResourceMethod,
    }


class CollectionListResource(BaseResource):
    path = 'collections/'

    methods = {
        'get': GetListResourceMethod,
        'search': SearchListResourceMethod,
    }


class CollectionOneResource(BaseResource):
    path = 'collections/'

    methods = {
        'get': GetOneResourceMethod,
        'create': CreateOneResourceMethod,
        'save': SaveOneResourceMethod,
        'update': UpdateOneResourceMethod,
        'remove': RemoveOneResourceMethod,
    }


class DocumentListResource(BaseResource):
    path = 'documents/'

    methods = {
        'get': GetListResourceMethod,
        'search': SearchListResourceMethod,
        'update': UpdateListResourceMethod,
        'upsert': UpsertListResourceMethod,
        'remove': RemoveListResourceMethod,
    }


class DocumentOneResource(BaseResource):
    path = 'documents/'

    methods = {
        'get': GetOneResourceMethod,
        'create': CreateOneResourceMethod,
        'save': SaveOneResourceMethod,
        'update': UpdateOneResourceMethod,
        'remove': RemoveOneResourceMethod,
    }
