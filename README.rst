django-dajaxice-ng
==================

.. image:: https://badge.fury.io/py/django-dajaxice-ng.png
    :target: http://badge.fury.io/py/django-dajaxice-ng

.. image:: https://travis-ci.org/ifanrx/django-dajaxice.png?branch=master
    :target: https://travis-ci.org/ifanrx/django-dajaxice

This is the next generation of dajaxice_ maintained by ifanrx_.

.. _dajaxice: https://github.com/jorgebastida/django-dajaxice
.. _ifanrx: https://github.com/ifanrx
Dajaxice is the communication core of dajaxproject. It's main goal is to trivialize the asynchronous communication within the django server side code and your js code.

dajaxice is JS-framework agnostic and focuses on decoupling the presentation logic from the server-side logic. dajaxice only requieres 5 minutes to start working.

Documentation
-------------
http://django-dajaxice-ng.readthedocs.org/quickstart.html


Django compatibility
--------------------
django-dajaxice Requires Django 1.7 or above.


Should I use django-dajaxice?
------------------------------
According to Jorge Bastida (https://github.com/jorgebastida),

    In a word, No. I created this project 4 years ago as a cool tool in order to solve one specific problem I had at that time.

    These days using this project is a bad idea.

    Perhaps I'm more pragmatic now, perhaps my vision of how my django projects should be coupled to libraries like this has change, or perhaps these days I really treasure the purity and simplicity of a vanilla django development.

    If you want to mimic what this project does, you would only need some simple views and jQuery.

    Forget about adding more unnecessary complexity.  Keep things simple.

And he has a point. However, what would you do if you are hired to add new features to a django app already built with dajaxice? Replace everything for jQuery (as Bastida suggests) or other technology? Find other guys interested and join forces to move the project forward? I chose the latter.

Project Aims
------------

  * Isolate the communication between the client and the server.
  * JS Framework agnostic (No Prototype, JQuery... needed ).
  * Presentation logic outside the views (No presentation code inside ajax functions).
  * Lightweight.
  * Crossbrowsing ready.
  * Unobtrusive standard-compliant (W3C) XMLHttpRequest 1.0 object usage.
  * Aggresive Django version support while regularly merging from upstream.

Running Tests
------------

.. code-block:: bash

   $ pip install -r dajaxice/tests/requirements.txt
   $ bash test_runner.sh
