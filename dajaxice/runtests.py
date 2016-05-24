#!/usr/bin/env python
import os
import sys

import django
from django.conf import settings
from django.test.utils import get_runner


if __name__ == "__main__":
    root_path = os.path.dirname((os.path.abspath(os.path.split(__file__)[0])))
    sys.path.insert(0, root_path)
    os.environ['DJANGO_SETTINGS_MODULE'] = 'dajaxice.tests.test_settings'
    # os.environ['DJANGO_SETTINGS_MODULE'] = 'tests.test_settings'

    django.setup()
    TestRunner = get_runner(settings)
    test_runner = TestRunner()
    failures = test_runner.run_tests(["dajaxice.tests"])
    sys.exit(bool(failures))
