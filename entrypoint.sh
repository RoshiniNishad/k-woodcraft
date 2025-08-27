#!/bin/sh
set -e

# Use the PORT env Railway provides (fallback to 8000)
: "${PORT:=8000}"

# Migrate, collectstatic, then start gunicorn
python manage.py migrate --noinput
python manage.py collectstatic --noinput

# Start Gunicorn (replace k_woodcraft with your django project package name)
exec gunicorn kwoodcraft.wsgi:application --bind 0.0.0.0:$PORT --workers 3
