#!/usr/bin/env bash
# exit on error
set -o errexit

source "./povenv/scripts/activate"

poetry install


python manage.py collectstatic --no-input
python manage.py migrate