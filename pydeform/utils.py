# -*- coding: utf-8 -*-
import datetime

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
        response = getattr(requests_session, method.lower())(**request_kwargs)
        if not response.ok and response.status_code not in ignore_error_codes:
            response.raise_for_status()
    except RequestException as e:
        error_class = None
        if e.response is not None:
            error_class = STATUS_CODE_ERROR_MAP.get(e.response.status_code)
        error_class = error_class or REQUESTS_ERROR_MAP.get(type(e)) or HTTPError
        raise error_class(requests_error=e)
    return response


def format_date(date):
    # todo: test me
    return format_datetime(
        datetime.datetime.combine(date, datetime.datetime.min.time())
    )


def format_datetime(date):
    """
    Convert datetime to UTC ISO 8601
    """
    # todo: test me
    if date.utcoffset() is None:
        return date.isoformat() + 'Z'

    utc_offset_sec = date.utcoffset()
    utc_date = date - utc_offset_sec
    utc_date_without_offset = utc_date.replace(tzinfo=None)
    return utc_date_without_offset.isoformat() + 'Z'


def flatten(data, prop_bits=None, result=None):
    if prop_bits is None:
        prop_bits = []
    if result is None:
        result = {}

    if not data:
        result = _set_flatten_result(data, prop_bits, result)
    elif isinstance(data, dict):
        for key, value in data.items():
            prop_bits.append((key, 'simple'))
            flatten(value, prop_bits=prop_bits, result=result)
            prop_bits.pop()
    elif isinstance(data, (list, tuple)):
        for key, value in enumerate(data):
            prop_bits.append((key, 'index'))
            flatten(value, prop_bits=prop_bits, result=result)
            prop_bits.pop()
    else:
        result = _set_flatten_result(data, prop_bits, result)

    return result


def _set_flatten_result(data, prop_bits, result):
    if prop_bits:
        result_key = ''
        for key, type_ in prop_bits:
            if type_ == 'index':
                result_key += '[%s]' % key
            else:
                result_key += '.%s' % key
        result[result_key.lstrip('.')] = data
    else:
        result = data
    return result
