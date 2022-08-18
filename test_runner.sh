#!/usr/bin/env bash

set -o errexit
set -o pipefail
# set -o xtrace

function is_lower_ver {
        ver=`echo -ne "$1\n$2" |sort -Vr |head -n1`
        if [ "$2" == "$1" ]; then
                return 1 
        elif [ "$2" == "$ver" ]; then
                return 1
        else
                return 0
        fi
}

django_ver=`python -c "import django; print(django.get_version())"`

# use app-test-runner for older versions of django
if is_lower_ver "1.7" "$django_ver"; then
    pip install https://github.com/jorgebastida/django-app-test-runner/zipball/master

    if echo $django_ver | grep ^1.6; then
        # for some reasons, django 1.6 requires this 
        tests=dajaxice.tests
    else
        tests=dajaxice
    fi

    app-test-runner dajaxice $tests
else
    # for django > 1.6, use the new test runner
    python dajaxice/runtests.py
fi
