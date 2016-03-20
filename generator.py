# -*- coding: utf-8 -*-
import sys
import os
import re
sys.path.append('../')

from jinja2 import Template

from pydeform import exceptions
from pydeform import Client
from pydeform.resources.base import BaseResource


BASE_PATH = os.path.dirname(os.path.normpath(__file__))
TEMPLATES_PATH = os.path.join(BASE_PATH, 'templates')
DEST_PATH = os.path.join(BASE_PATH)


def _render_and_save_template(path, context):
    template_path = os.path.join(TEMPLATES_PATH, path + '.tpl')
    destination_path = os.path.join(BASE_PATH, path + '.md')
    with open(destination_path, 'wt') as dest_file:
        dest_file.write(
            Template(open(template_path).read()).render(context)
        )


def _prepare_docstring(value):
    if not value:
        return ''
    remove_spaces = 0
    for line in value.split('\n')[1:]:
        if line:
            for char in line:
                if char != ' ':
                    break
                else:
                    remove_spaces += 1
            break

    return re.sub(
        r'^ {%s}' % remove_spaces,
        '',
        unicode(value),
        flags=re.MULTILINE
    ).strip()


def generate_api_reference():
    generate_client_api_reference()
    generate_exceptions_api_reference()


def generate_client_api_reference():
    client = Client('deform.io')
    session_auth_client = client.auth('session', 'noop')
    project_client = session_auth_client.use_project('noop')
    clients = [
        (client, ['auth']),
        (session_auth_client, ['use_project']),
        (project_client, []),
    ]

    _render_and_save_template(
        'api/client',
        {
            'clients': map(_get_client_for_doc, clients)
        }
    )


def _get_client_for_doc(client_info):
    # for name, resource in get_resources(client_instance):
    #     doc_file.write(resource._get_docs(name))
    client = client_info[0]
    document_methods = client_info[1]

    return {
        'name': type(client).__name__,
        'doc': _prepare_docstring(client.__doc__),
        'methods': [
            {
                'name': i,
                'doc': _prepare_docstring(getattr(client, i).__doc__)
            } for i in document_methods
        ],
        'resources': map(_get_resource_for_doc, _get_client_resources(client))
    }


def _get_client_resources(client_instance):
    return [
        {
            'name': i,
            'instance': getattr(client_instance, i)
        }
        for i in dir(client_instance)
        if isinstance(getattr(client_instance, i), BaseResource)
    ]


def _get_resource_for_doc(resource):
    return {
        'name': resource['name'],
        'doc': _prepare_docstring(resource['instance'].__doc__),
        'methods': map(
            _get_resoure_method_for_doc,
            resource['instance'].get_methods().items()
        )
    }


def _get_resoure_method_for_doc(method_info):
    method_name = method_info[0]
    method_instance = method_info[1]

    return {
        'name': method_name,
        'doc': _prepare_docstring(method_instance.__doc__),
        'params': _get_resource_method_params_for_doc(method_instance)
    }


def _get_resource_method_params_for_doc(method):
    params_required = method.get_params_required()
    response = []
    for name, param in method.get_params_definitions().items():
        response.append({
            'name': name,
            'description': param.get('description'),
            'required': name in params_required
        })
    return sorted(response, key=lambda x: not x['required'])


def generate_exceptions_api_reference():
    doc_exceptions = [
        exceptions.DeformException,
        exceptions.HTTPError
    ]
    for attr in dir(exceptions):
        obj = getattr(exceptions, attr)
        try:
            if (issubclass(obj, exceptions.DeformException) and
                obj not in doc_exceptions):
                doc_exceptions.append(obj)
        except TypeError:
            pass  # if obj is not class
    _render_and_save_template(
        'api/exceptions',
        {
            'exceptions': map(_get_exception_for_doc, doc_exceptions)
        }
    )


def _get_exception_for_doc(exc):
    return {
        'name': exc.__name__,
        'doc': _prepare_docstring(exc.__doc__),
        'bases': [i.__name__ for i in exc.__bases__]
    }
