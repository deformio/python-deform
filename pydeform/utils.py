# -*- coding: utf-8 -*-
from requests.exceptions import RequestException

from pydeform.exceptions import (
    HTTPError,
    STATUS_CODE_ERROR_MAP,
    REQUESTS_ERROR_MAP
)


def get_base_uri(host,
                 api_base_path,
                 port=None,
                 secure=True,
                 project=None):
    return ''.join([
        i for i in [
            'https://' if secure else 'http://',
            '%s.' % project if project else None,
            host,
            ':%s' % port if port else None,
            api_base_path
        ] if i
    ])


def uri_join(*parts):
    if parts[0].endswith('://'):
        schema_list = [parts[0][:-1]]
        parts = parts[1:]
    else:
        schema_list = []
    add_last_dash = parts[-1][-1] == '/'
    response = '/'.join(schema_list + [i.strip('/') for i in parts])
    if add_last_dash:
        response += '/'
    return response


def do_http_request(requests_session,
                    method='get',
                    request_kwargs=None,
                    ignore_error_codes=[]):
    # todo: test me
    if request_kwargs is None:
        request_kwargs = {}
    try:
        response = getattr(requests_session, method)(**request_kwargs)
        if not response.ok and response.status_code not in ignore_error_codes:
            response.raise_for_status()
    except RequestException as e:
        error_class = None
        if e.response is not None:
            error_class = STATUS_CODE_ERROR_MAP.get(e.response.status_code)
        error_class = error_class or REQUESTS_ERROR_MAP.get(type(e)) or HTTPError
        raise error_class(requests_error=e)
    return response
