#!/bin/sh
set -e

echo "Running database migrations..."
python manage.py makemigrations
python manage.py migrate --noinput

echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Starting Gunicorn..."
exec gunicorn Lenders.wsgi:application \
    --bind 0.0.0.0:${PORT:-10000} \
    --workers 3 \
    --timeout 120