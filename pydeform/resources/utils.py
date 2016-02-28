# -*- coding: utf-8 -*-
import datetime
from copy import deepcopy
from collections import defaultdict

from pydeform.utils import (
    uri_join,
    format_date,
    format_datetime,
    flatten,
)


PARAMS_DEFINITIONS = {
    'identity': {
        'name': 'identity',
        'dest': 'uri'
    },
    'property': {
        'name': 'property',
        'default': [],
        'dest': 'uri'
    },
    'fields': {
        'name': 'fields',
        'default': [],
        'dest': 'query_params',
    },
    'fields_exclude': {
        'name': 'fields_exclude',
        'default': [],
        'dest': 'query_params',
    },
    'data': {
        'name': 'data',
        'dest': 'payload'
    },
}

URI_PARAMS_ORDER = [
    'identity',
    'property'
]


def get_params_by_destination(params, definitions):
    response = defaultdict(dict)
    for param_key, param_value in params.items():
        response[
            definitions[param_key]['dest']
        ][param_key] = param_value
    return response


def get_url(base_uri, params, definitions, uri_params_order):
    uri_bits = [base_uri]

    for param_name in uri_params_order:
        value = params.get(param_name)
        if value:
            if isinstance(value, list):
                uri_bits += value
            else:
                uri_bits.append(value)

    return '%s/' % uri_join(*uri_bits).rstrip('/')


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
    assert 'data' in definitions
    assert definitions['data']['dest'] == 'payload'

    with_files, prepared_data = _prepare_payload(params['data'])
    if with_files:
        prepared_data = flatten(prepared_data)
    return {
        'type': 'files' if with_files else 'json',
        'data': prepared_data
    }
    

def _prepare_payload(data):
    if isinstance(data, datetime.datetime):
        return False, format_datetime(data)
    elif isinstance(data, datetime.date):
        return False, format_date(data)
    elif isinstance(data, (list, tuple)):
        items = []
        items_with_files = False
        for i in data:
            with_files, response = _prepare_payload(i)
            items.append(response)
            if with_files and not items_with_files:
                items_with_files = True
        return items_with_files, type(data)(items)
    elif isinstance(data, dict):
        items = []
        items_with_files = False
        for key, value in data.items():
            with_files, response = _prepare_payload(value)
            items.append((key, response))
            if with_files and not items_with_files:
                items_with_files = True
        return items_with_files, dict(items)
    elif isinstance(data, file):
        return True, data
    else:
        return False, data
