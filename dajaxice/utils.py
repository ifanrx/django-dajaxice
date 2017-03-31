from django.http import QueryDict


def deserialize_form(data):
    """
    Create a new QueryDict from a serialized form.
    """
    return QueryDict(query_string=str(data).encode('utf-8'))
