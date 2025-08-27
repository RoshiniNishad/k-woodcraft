# Use a lightweight Python image
FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Install system deps for Pillow/psycopg2 etc.
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential libpq-dev gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy and install python deps
COPY requirements.txt /app/requirements.txt
RUN pip install --upgrade pip
RUN pip install -r /app/requirements.txt

# Copy project
COPY . /app

# Make entrypoint executable (entrypoint will run migrations, collectstatic, then start gunicorn)
RUN chmod +x /app/entrypoint.sh

# Expose the port Railway expects (Railway provides $PORT) — we'll bind to $PORT at runtime
EXPOSE 8000

# Start the app via entrypoint script
CMD ["/app/entrypoint.sh"]
