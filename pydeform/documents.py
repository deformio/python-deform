

class Documents(object):
    def find(query, fields=None, exclude_fields=None, sort=None, pagination=None):
        return self.paginator.get_response(
            base_uri=base_uri
        )
