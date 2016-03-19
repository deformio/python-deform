# -*- coding: utf-8 -*-


def get_session_http_auth_header(session_id):
    return 'SessionId %s' % session_id


def get_token_http_auth_header(token):
    return 'Token %s' % token
