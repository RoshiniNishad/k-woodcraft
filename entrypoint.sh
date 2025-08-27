#!/bin/sh
set -e

# Use the PORT env Railway provides (fallback to 8000)
: "${PORT:=8000}"

# Run database migrations
python manage.py migrate --noinput

# Collect static files
python manage.py collectstatic --noinput

# Create superuser if it doesn’t exist (using Railway env vars)
if [ "$DJANGO_SUPERUSER_USERNAME" ] && [ "$DJANGO_SUPERUSER_EMAIL" ]; then
    python manage.py shell << END
from django.contrib.auth import get_user_model
User = get_user_model()
username = "${DJANGO_SUPERUSER_USERNAME}"
email = "${DJANGO_SUPERUSER_EMAIL}"
password = "${DJANGO_SUPERUSER_PASSWORD}"

if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username=username, email=email, password=password)
    print("Superuser created: ", username)
else:
    print("Superuser already exists: ", username)
END
fi

# Start Gunicorn (replace kwoodcraft with your django project package name)
exec gunicorn kwoodcraft.wsgi:application --bind 0.0.0.0:$PORT --workers 3
