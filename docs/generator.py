# -*- coding: utf-8 -*-
import sys
import os
import re
sys.path.append('../')

from jinja2 import Template

from pydeform import exceptions
from pydeform import Client


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
    return re.sub(r'^    ', '', unicode(value), flags=re.MULTILINE).strip()


def generate_api_reference():
    generate_exceptions_api_reference()

    # client = Client('deform.io')
    # session_auth_client = client.auth('session', 'noop')
    # project_client = session_auth_client.use_project('noop')

    # for client_instance, filename in [
    #     (client, 'client'),
    #     (session_auth_client, 'session_auth_client'),
    #     (project_client, 'project_client'),
    # ]:
    #     with open(
    #         os.path.join(
    #             DOCS_CONFIG['client_generated_docs_sourcedir'],
    #             filename + '.rst'
    #         ),
    #         'wt'
    #     ) as doc_file:
    #         for name, resource in get_resources(client_instance):
    #             doc_file.write(resource._get_docs(name))


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
