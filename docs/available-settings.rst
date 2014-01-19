Available Settings
==================

DAJAXICE_MEDIA_PREFIX
---------------------

This will be the namespace that dajaxice will use as endpoint.

Defaults to ``dajaxice``

Optional: ``True``

DAJAXICE_XMLHTTPREQUEST_JS_IMPORT
---------------------------------

Include XmlHttpRequest.js inside dajaxice.core.js

Defaults to ``False``

Optional: ``True``

DAJAXICE_JSON2_JS_IMPORT
------------------------

Include json2.js inside dajaxice.core.js

Defaults to ``False``

Optional: ``True``

DAJAXICE_EXCEPTION
------------------

Default data sent when an exception occurs.

Defaults to ``"DAJAXICE_EXCEPTION"``

Optional: ``True``

DAJAXICE_NOT_CALLABLE_RESPONSE
------------------------------

Response when requested a non-callable method (e.g used ``GET`` when ``POST`` is desired).

Defaults to ``{"error":"400 Bad Request"}``

Optional: ``True``

DAJAXICE_IGNORE_REQUEST_NOT_IN_CONTEXT
--------------------------------------

**Not recommended. Use at your own risk.**

By default, when ``request`` was not found in ``context``, Dajaxice will complain by raising warning message. In rare cases, you don't always have ``requset`` in ``context`` (for example in 404 handlers). Set to ``True`` will surpress such warnings.

Defaults to ``False``

Optional: ``True``
