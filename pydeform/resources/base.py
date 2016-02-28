# -*- coding: utf-8 -*-
from pydeform.utils import (
    uri_join,
    do_http_request,
)
# from pydeform.resources.utils import (
#     PARAMS_DEFINITIONS
# )


class BaseResource(object):
    path = ''
    methods = {}

    def __init__(self, base_uri, auth_header, requests_session):
        kwargs = {
            'base_uri': uri_join(base_uri, self.path),
            'auth_header': auth_header,
            'requests_session': requests_session
        }
        for method_name, method_factory in self.methods:
            setattr(self, method_name, method_factory(**kwargs))


class ResourceMethodBase(object):
    method = None
    action = None
    params = {}

    def __init__(self,
                 base_uri,
                 auth_header,
                 requests_session):
        self.base_uri = base_uri
        self.auth_header = auth_header
        self.requests_session = requests_session
        if not any(self.method, self.action):
            raise ValueError('You should specify method or action')
        if self.action:
            self.method = 'post'

    def __call__(self,
                 timeout=None,
                 **params):
        context = self.get_context(params)
        context['timeout'] = timeout
        if action:
            context['headers']['X-Action'] = action
        response = do_http_request(
            method=self.method,
            requests_kwargs=context
        )
        return response.json()['result']

    def get_context(self, params):
        params_by_destination = get_params_by_destination(params)
        payload = get_payload(params_by_destination.get('payload'))
        context = {
            'url': get_url(base_uri, params_by_destination.get('url')),
            'headers': get_headers(params_by_destination.get('headers')),
            'query_params': get_query_params(params_by_destination.get('query_params')),
        }
        if payload:
            context[payload['type']] = payload['data']
        return context


class ListResourceMethodBase(ResourceMethodBase):
    pass


class GetListResourceMethod(ListResourceMethodBase):
    method = 'get'


class SearchListResourceMethod(ListResourceMethodBase):
    def __call__(self,
                 search_filter=None,
                 search_text=None,
                 **kwargs):
        pass


class OneResourceMethodBase(ResourceMethodBase):
    pass

# class GetOneResourceMethod(ResourceMethodBase):
#     def __call__(self,
#                  identity=True,
#                  **kwargs):
#         pass
