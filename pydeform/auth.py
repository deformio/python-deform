# -*- coding: utf-8 -*-
from pydeform.utils import uri_join, do_http_request


def get_session_id(base_uri, email, password, requests_session, timeout=None):
    response = do_http_request(
        requests_session=requests_session,
        method='post',
        request_kwargs={
            'url': uri_join(base_uri, '/user/'),
            'headers': {
                'X-Action': 'Login'
            },
            'json': {
                'payload': {
                    'email': email,
                    'password': password
                }
            },
            'timeout': timeout
        }
    )
    return response.json()['result']['sessionId']


def get_session_http_auth_header(session_id):
    return 'SessionId %s' % session_id


def get_token_http_auth_header(token):
    return 'Token %s' % token
