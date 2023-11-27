
#!/usr/bin/env bash
# exit on error
set -o errexit

poetry install

RENDER="python manage.py collectstatic --no-input"
$RENDER
python manage.py migrate