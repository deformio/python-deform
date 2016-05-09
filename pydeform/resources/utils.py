# -*- coding: utf-8 -*-
import datetime
from collections import defaultdict

from pydeform.exceptions import NotFoundError
from pydeform.six import PY2
from pydeform.utils import (
    do_http_request,
    flatten,
    format_date,
    format_datetime,
    uri_join
)

PARAMS_DEFINITIONS = {
    'login_email': {
        'dest': 'payload',
        'payload_property': 'email',
        'description': 'User email'
    },
    'login_password': {
        'dest': 'payload',
        'payload_property': 'password',
        'description': 'User password'
    },
    'confirm_code': {
        'dest': 'payload',
        'payload_property': 'code',
        'description': 'Email confirmation code'
    },
    'identity': {
        'dest': 'uri',
        'description': 'Identity'
    },
    'collection': {
        'dest': 'uri',
        'description': 'Collection'
    },
    'property': {
        'dest': 'uri',
        'description': 'Work with specified property'
    },
    'fields': {
        'dest': 'query_params',
        'description': 'Return specified fields only'
    },
    'fields_exclude': {
        'dest': 'query_params',
        'description': 'Return all but the excluded field'
    },
    'data': {
        'dest': 'payload',
        'description': 'Data'
    },
    'find_filter': {
        'dest': 'payload',
        'payload_property': 'filter',
        'description': 'Filter query'
    },
    'find_text': {
        'dest': 'payload',
        'payload_property': 'text',
        'description': 'Full text search value'
    },
    'update_operation': {
        'dest': 'payload',
        'payload_property': 'operation',
        'description': 'Update operation'
    },
    'page': {
        'dest': 'query_params',
        'page': 'Page number'
    },
    'per_page': {
        'dest': 'query_params',
        'page': 'Items per page'
    },
    'sort': {
        'dest': 'query_params',
        'page': 'Sort by property'
    },
}

if PY2:
    FILE_TYPE = file
else:
    from io import IOBase
    FILE_TYPE = IOBase


def get_params_by_destination(params, definitions):
    response = defaultdict(dict)
    for param_key, param_value in params.items():
        response[
            definitions[param_key]['dest']
        ][param_key] = param_value
    return response


def get_url(base_uri, path, params, definitions):
    # todo: retest me
    uri_bits = [base_uri]

    for path_item in path:
        if path_item.startswith('{'):
            path_item_var_name = path_item.strip('{}')
            value = params.get(path_item_var_name)
        else:
            value = path_item

        if value:
            if isinstance(value, list):
                uri_bits += value
            else:
                uri_bits.append(value)
    uri_bits.append('/')

    return uri_join(*uri_bits)


def get_headers(auth_header, params, definitions):
    return {
        'Authorization': auth_header
    }


def get_query_params(params, definitions):
    response = {}
    for key, value in params.items():
        if isinstance(value, (list, tuple)):
            value = ','.join(value)
        response[key] = value
    return response


def get_payload(params, definitions):
    if not params:
        return

    params_has_files = False
    final_data = {}

    for key, value in params.items():
        with_files, prepared_data = prepare_payload(value)
        if with_files:
            params_has_files = True
        payload_property = definitions.get(key).get('payload_property')
        if payload_property:
            final_data[payload_property] = prepared_data
        else:
            final_data = prepared_data

    if params_has_files:
        if isinstance(final_data, FILE_TYPE):
            final_data = {
                'file': final_data
            }
        else:
            final_data = flatten(final_data)
            for key, value in final_data.items():
                if not isinstance(value, FILE_TYPE):
                    final_data[key] = (None, value)
    else:
        final_data = {
            'payload': final_data
        }
    return {
        'type': 'files' if with_files else 'json',
        'data': final_data
    }


def prepare_payload(data):
    if isinstance(data, datetime.datetime):
        return False, format_datetime(data)
    elif isinstance(data, datetime.date):
        return False, format_date(data)
    elif isinstance(data, (list, tuple)):
        items = []
        items_with_files = False
        for i in data:
            with_files, response = prepare_payload(i)
            items.append(response)
            if with_files and not items_with_files:
                items_with_files = True
        return items_with_files, type(data)(items)
    elif isinstance(data, dict):
        items = []
        items_with_files = False
        for key, value in data.items():
            with_files, response = prepare_payload(value)
            items.append((key, response))
            if with_files and not items_with_files:
                items_with_files = True
        return items_with_files, dict(items)
    elif isinstance(data, FILE_TYPE):
        return True, data
    else:
        return False, data


def iterate_by_pagination(method,
                          request_kwargs,
                          requests_session,
                          request_defaults):
    response_result = {
        'links': {
            'next': 'yes'
        }
    }
    page = 0
    if 'params' not in request_kwargs:
        request_kwargs['params'] = {}
    while True:
        if response_result.get('links', {}).get('next'):
            page += 1
            request_kwargs['params']['page'] = page
            response = do_http_request(
                method=method,
                request_kwargs=request_kwargs,
                requests_session=requests_session,
                request_defaults=request_defaults,
            )
            response_result = response.json()['result']
            if response_result['items']:
                for i in response_result['items']:
                    yield i
            else:
                break
        else:
            break
