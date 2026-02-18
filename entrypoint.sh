#!/bin/sh

# Вивести інформацію про запуск
echo "Starting CS2 MicroTwitter application..."

# Виконати міграції бази даних
echo "Running database migrations..."
python manage.py migrate --noinput

# Зібрати статичні файли (якщо ще не зроблено)
echo "Collecting static files..."
python manage.py collectstatic --noinput

# Запустити Gunicorn
echo "Starting Gunicorn server..."
exec gunicorn group_project.wsgi:application \
    --bind 0.0.0.0:8000 \
    --workers 4 \
    --timeout 120 \
    --access-logfile - \
    --error-logfile - \
    --log-level info