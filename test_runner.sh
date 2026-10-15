#!/usr/bin/env bash

set -o errexit
set -o pipefail

PYTHON="${PYTHON:-python3}"

exec "$PYTHON" dajaxice/runtests.py "$@"
