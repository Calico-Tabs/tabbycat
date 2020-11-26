#!/bin/bash
source /var/app/venv/*/bin/activate
export PYTHONPATH=/var/app/venv/staging-LQM1lest/bin:/var/app/staging/tabbycat
export DJANGO_SETTINGS_MODULE=settings

echo "-----> Running database migration"
python manage.py migrate_schemas --noinput

echo "-----> Running dynamic preferences checks"
python manage.py checkpreferences_schemas --tenant

echo "-----> Running static asset compilation"
npm install -g @vue/cli-service-global
npm run build

echo "-----> Running static files compilation"
python manage.py collectstatic --noinput
