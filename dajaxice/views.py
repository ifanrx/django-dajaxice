import json
import logging

from django.conf import settings
from django.http import Http404, HttpResponse
from django.views.generic.base import View

from dajaxice.core import dajaxice_config, dajaxice_functions
from dajaxice.exceptions import FunctionNotCallableError

log = logging.getLogger('dajaxice')


class DajaxiceRequest(View):
    """ Handle all the dajaxice xhr requests. """

    def dispatch(self, request, name=None, *args, **kwargs):

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
                except (json.decoder.JSONDecodeError, ValueError):
                    log.exception('name=%s, data=%s', name, data)
                    data = {}
            else:
                data = {}

            # Call the function. If something goes wrong, handle the Exception
            try:
                response = func.call(request, **data)
            except Exception:
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
