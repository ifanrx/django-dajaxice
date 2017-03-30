import os
import sys

import django
from django.conf import settings

# test runner heavily based on http://stackoverflow.com/a/12260597

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.dirname(BASE_DIR))


if __name__ == "__main__":
    settings.configure(DEBUG=True,
                       DATABASES={
                           'default': {
                               'ENGINE': 'django.db.backends.sqlite3',
                           }
                       },
                       ROOT_URLCONF='dajaxice.urls',
                       INSTALLED_APPS=('django.contrib.auth',
                                       'django.contrib.contenttypes',
                                       'django.contrib.sessions',
                                       'django.contrib.admin',
                                       'dajaxice',
                                       'dajaxice.tests',))


    django.setup()
    from django.test.runner import DiscoverRunner

    test_runner = DiscoverRunner(verbosity=1)

    failures = test_runner.run_tests(['dajaxice.tests'], verbosity=1)

    if failures:
        sys.exit(failures)
