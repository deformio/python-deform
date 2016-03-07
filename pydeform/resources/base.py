# -*- coding: utf-8 -*-
from copy import deepcopy

from pydeform.utils import (
    uri_join,
    do_http_request,
)
from pydeform.resources.utils import (
    PARAMS_DEFINITIONS,
    URI_PARAMS_ORDER,
    get_params_by_destination,
    get_url,
    get_payload,
    get_headers,
    get_query_params,
    iterate_by_pagination,
)


class BaseResource(object):
    path = []
    methods = {}

    def __init__(self, base_uri, auth_header, requests_session, request_defaults):
        kwargs = {
            'base_uri': uri_join(base_uri, *self.path + ['/']),
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
    uri_params_order = URI_PARAMS_ORDER
    return_create_status = False

    def __init__(self,
                 base_uri,
                 auth_header,
                 requests_session,
                 request_defaults):
        self.base_uri = base_uri
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
                return self._prepare_paginated_response(response.json())
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
            if response.content:
                result = response.json()['result']
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
            'result': response['result'],
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
                params=params_by_destination.get('uri', {}),
                definitions=params_definitions,
                uri_params_order=self.get_uri_params_order()
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
        for key, value in context.items():
            if not value:
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

    def get_uri_params_order(self):
        # todo: test me
        return deepcopy(self.uri_params_order)

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
    method = 'delete'
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


class CreateOneResourceMethod(ResourceMethodBase):
    method = 'post'
    params = {
        'property': PARAMS_DEFINITIONS['property'],
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


class UpdateOneResourceMethod(ResourceMethodBase):
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
