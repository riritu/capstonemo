#!/usr/bin/env bash
# exit on error
set -o errexit

poetry install

python manage.py create_generic_user

python manage.py collectstatic --no-input
python manage.py makemigrations

python manage.py migrate
