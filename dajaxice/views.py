import logging
from django.conf import settings
from django.views.generic.base import View
from django.http import HttpResponse, Http404

from dajaxice.exceptions import FunctionNotCallableError
from dajaxice.core import dajaxice_functions, dajaxice_config

import json


log = logging.getLogger('dajaxice')


class DajaxiceRequest(View):
    """ Handle all the dajaxice xhr requests. """

    def dispatch(self, request, name=None):

        if not name:
            raise Http404

        # Check if the function is callable
        if dajaxice_functions.is_callable(name, request.method):

            func = dajaxice_functions.get(name)
            data = getattr(request, func.method).get('argv', 'undefined')

            # Clean the argv
            if data != 'undefined':
                try:
                    data = json.loads(data)
                except json.decoder.JSONDecodeError:
                    log.exception('name=%s, data=%s', name, data)
                    data = {}
            else:
                data = {}

            # Call the function. If something goes wrong, handle the Exception
            try:
                response = func.call(request, **data)
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
