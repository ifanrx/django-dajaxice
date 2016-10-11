import logging
from django.conf import settings
from django.views.generic.base import View
from django.http import HttpResponse, Http404

from dajaxice.exceptions import FunctionNotCallableError
from dajaxice.core import dajaxice_functions, dajaxice_config

import json

log = logging.getLogger('dajaxice')


def safe_dict(d):
    """
    Recursively clone json structure with UTF-8 dictionary keys
    http://www.gossamer-threads.com/lists/python/bugs/684379
    """
    if isinstance(d, dict):
        return dict(
            [(k.encode('utf-8'), safe_dict(v)) for k, v in d.iteritems()])
    elif isinstance(d, list):
        return [safe_dict(x) for x in d]
    else:
        return d


class DajaxiceRequest(View):
    """ Handle all the dajaxice xhr requests. """

    def dispatch(self, request, name=None):

        if not name:
            raise Http404

        # Check if the function is callable
        if dajaxice_functions.is_callable(name, request.method):

            function = dajaxice_functions.get(name)
            data = getattr(request, function.method).get('argv', '')

            # Clean the argv
            if data != 'undefined':
                try:
                    data = safe_dict(json.loads(data))
                except Exception:
                    data = {}
            else:
                data = {}

            # Call the function. If something goes wrong, handle the Exception
            try:
                response = function.call(request, **data)
            except:
                log.exception('name=%s, data=%s', name, data)
                if settings.DEBUG:
                    raise FunctionNotCallableError
                response = dajaxice_config.DAJAXICE_EXCEPTION

            return HttpResponse(
                response, content_type="application/x-json; charset=utf-8")
        else:
            if settings.DEBUG:
                raise FunctionNotCallableError
            log.error('Function %s is not callable. method=%s', name,
                      request.method)
            return HttpResponse(
                dajaxice_config.DAJAXICE_NOT_CALLABLE_RESPONSE,
                content_type="application/json; charset=utf-8")
