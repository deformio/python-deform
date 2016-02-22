# -*- coding: utf-8 -*-
from pydeform.documents import Documents
from pydeform.utils import uri_join


class Collections(object):
    def __init__(self, base_uri):
        self.base_uri = base_uri

    def __call__(self, identity_or_query=None):
        if not isinstance(identity_or_query, dict):
            return Collection(
                base_uri=uri_join(uri_join(self.base_uri, identity))
            )
        else:
            return iterator(identity_or_query)


class Collection(object):
    def __init__(self, base_uri):
        self.base_uri = base_uri
        self.documents = Documents(
            base_uri=uri_join(base_uri, 'documents')
        )
