#!/bin/bash

# Виконати міграції
python manage.py migrate --noinput

# Запустити Gunicorn
exec gunicorn --bind 0.0.0.0:$PORT group_project.wsgi:application