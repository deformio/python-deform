# -*- coding: utf-8 -*-
from copy import deepcopy

from pydeform.resources.utils import (
    PARAMS_DEFINITIONS,
    get_headers,
    get_params_by_destination,
    get_payload,
    get_query_params,
    get_url,
    iterate_by_pagination
)
from pydeform.utils import do_http_request, uri_join


class BaseResource(object):
    path = []
    methods = {}

    def __init__(self,
                 base_uri,
                 auth_header,
                 requests_session,
                 request_defaults):
        kwargs = {
            'base_uri': base_uri,
            'path': self.path,
            'auth_header': auth_header,
            'requests_session': requests_session,
            'request_defaults': request_defaults,
        }
        for method_name, method_factory in self.methods.items():
            setattr(self, method_name, method_factory(**kwargs))

    def get_methods(self):
        response = {}
        for method_name in self.methods.keys():
            response[method_name] = getattr(self, method_name)
        return response


class ResourceMethodBase(object):
    method = None
    action = None
    params = {}
    params_required = []
    is_paginatable = False
    pagination_params = {
        'page': PARAMS_DEFINITIONS['page'],
        'per_page': PARAMS_DEFINITIONS['per_page'],
    }
    return_create_status = False
    result_property = None

    def __init__(self,
                 base_uri,
                 path,
                 auth_header,
                 requests_session,
                 request_defaults):
        self.base_uri = base_uri
        self.path = path
        self.auth_header = auth_header
        self.requests_session = requests_session
        self.request_defaults = request_defaults
        if not any([self.method, self.action]):
            raise ValueError('You should specify method or action')
        if self.action:
            self.method = 'post'

    def __call__(self,
                 timeout=None,
                 **params):
        for param_required in self.get_params_required():
            if param_required not in params:
                raise ValueError('%s is required parameter' % param_required)
        context = self.get_context(params)
        context['timeout'] = timeout
        if self.is_paginatable:
            if self._pagination_is_activated(context):
                response = do_http_request(
                    method=self.method,
                    request_kwargs=context,
                    requests_session=self.requests_session,
                    request_defaults=self.request_defaults,
                )
                return self._prepare_paginated_response(
                    response.json()['result']
                )
            else:
                return iterate_by_pagination(
                    method=self.method,
                    request_kwargs=context,
                    requests_session=self.requests_session,
                    request_defaults=self.request_defaults,
                )
        else:
            response = do_http_request(
                method=self.method,
                request_kwargs=context,
                requests_session=self.requests_session,
                request_defaults=self.request_defaults,
            )
            if context.get('stream'):
                return response.raw

            if response.content:
                try:
                    result = response.json()['result']
                    if self.result_property:
                        result = result[self.result_property]
                except ValueError:
                    result = response.content
            else:
                result = None

            if self.return_create_status:
                return {
                    'created': response.status_code == 201,
                    'result': result
                }
            else:
                return result

    def _pagination_is_activated(self, context):
        for pagination_param in self.pagination_params:
            if pagination_param in context.get('params', {}):
                return True

    def _prepare_paginated_response(self, response):
        return {
            'page': response['page'],
            'pages': response['pages'],
            'per_page': response['per_page'],
            'total': response['total'],
            'items': response['items'],
        }

    def get_context(self, params):
        params_definitions = self.get_params_definitions()
        params_by_destination = get_params_by_destination(
            params,
            definitions=params_definitions
        )
        context = {
            'url': get_url(
                base_uri=self.base_uri,
                path=self.path,
                params=params_by_destination.get('uri', {}),
                definitions=params_definitions,
            ),
            'headers': get_headers(
                auth_header=self.auth_header,
                params=params_by_destination.get('headers', {}),
                definitions=params_definitions,
            ),
            'params': get_query_params(
                params=params_by_destination.get('query_params', {}),
                definitions=params_definitions,
            ),
        }
        delete_keys = []
        for key, value in context.items():
            if not value:
                delete_keys.append(key)
        for key in delete_keys:
            del context[key]

        payload = get_payload(
            params_by_destination.get('payload'),
            definitions=params_definitions
        )
        if self.action:
            context['headers']['X-Action'] = self.action
        if payload:
            context[payload['type']] = payload['data']
        else:
            context['headers']['Content-Type'] = 'application/json'
        return context

    def get_params_definitions(self):
        # todo: test me
        params_definitions = deepcopy(self.params)
        if self.is_paginatable:
            params_definitions.update(self.pagination_params)
        return params_definitions

    def get_params_required(self):
        # todo: test me
        return deepcopy(self.params_required)


class GetListResourceMethod(ResourceMethodBase):
    method = 'get'
    is_paginatable = True
    params = {
        'fields': PARAMS_DEFINITIONS['fields'],
        'fields_exclude': PARAMS_DEFINITIONS['fields_exclude'],
        'sort': PARAMS_DEFINITIONS['sort'],
    }


class FindListResourceMethod(ResourceMethodBase):
    action = 'find'
    is_paginatable = True
    params = {
        'filter': PARAMS_DEFINITIONS['find_filter'],
        'text': PARAMS_DEFINITIONS['find_text'],
        'sort': PARAMS_DEFINITIONS['sort'],
    }


class CountListResourceMethod(ResourceMethodBase):
    action = 'find'
    params = {
        'filter': PARAMS_DEFINITIONS['find_filter'],
        'text': PARAMS_DEFINITIONS['find_text'],
    }

    def __call__(self,
                 timeout=None,
                 **params):
        context = self.get_context(params)
        context['timeout'] = timeout
        if 'params' not in context:
            context['params'] = {}
        context['params']['per_page'] = 1
        context['params']['fields'] = '_id'

        response = do_http_request(
            method=self.method,
            request_kwargs=context,
            requests_session=self.requests_session,
            request_defaults=self.request_defaults,
        )
        response = response.json()
        return response['result']['total']


class UpdateListResourceMethod(ResourceMethodBase):
    action = 'update'
    params = {
        'filter': PARAMS_DEFINITIONS['find_filter'],
        'operation': PARAMS_DEFINITIONS['update_operation']
    }
    params_required = ['operation']


class UpsertListResourceMethod(UpdateListResourceMethod):
    action = 'upsert'


class RemoveListResourceMethod(ResourceMethodBase):
    action = 'delete'
    params = {
        'filter': PARAMS_DEFINITIONS['find_filter'],
    }


class GetResourceMethod(ResourceMethodBase):
    method = 'get'


class GetOneResourceMethod(ResourceMethodBase):
    method = 'get'
    params = {
        'identity': PARAMS_DEFINITIONS['identity'],
        'property': PARAMS_DEFINITIONS['property'],
    }
    params_required = ['identity']


class GetFileResourceMethod(GetOneResourceMethod):
    method = 'get'

    def get_context(self, params):
        context = super(GetFileResourceMethod, self).get_context(params)
        context['stream'] = True
        context['url'] = uri_join(context['url'], 'content/')
        return context


class CreateOneResourceMethod(ResourceMethodBase):
    method = 'post'
    params = {
        'data': PARAMS_DEFINITIONS['data'],
    }
    params_required = ['data']


class SaveOneResourceMethod(ResourceMethodBase):
    method = 'put'
    params = {
        'identity': PARAMS_DEFINITIONS['identity'],
        'property': PARAMS_DEFINITIONS['property'],
        'data': PARAMS_DEFINITIONS['data'],
    }
    params_required = ['data']
    return_create_status = True


class UpdateResourceMethod(ResourceMethodBase):
    method = 'patch'

    params = {
        'data': PARAMS_DEFINITIONS['data'],
    }
    params_required = ['data']


class UpdateOneResourceMethod(UpdateResourceMethod):
    method = 'patch'
    params = {
        'identity': PARAMS_DEFINITIONS['identity'],
        'property': PARAMS_DEFINITIONS['property'],
        'data': PARAMS_DEFINITIONS['data'],
    }
    params_required = ['identity', 'data']


class RemoveOneResourceMethod(ResourceMethodBase):
    method = 'delete'
    params = {
        'identity': PARAMS_DEFINITIONS['identity'],
        'property': PARAMS_DEFINITIONS['property'],
    }
    params_required = ['identity']
