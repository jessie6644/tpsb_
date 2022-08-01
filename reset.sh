#!/bin/bash

# Script for quickly resetting the Django environment to a clean slate
rm -f db.sqlite3
rm -f meetings/migrations/0*.py
python manage.py makemigrations
python manage.py migrate
DJANGO_SUPERUSER_PASSWORD=admin python manage.py createsuperuser --username admin --email admin@example.com --noinput
python manage.py loaddata meetings/fixtures/*.json

rm -rf uploads