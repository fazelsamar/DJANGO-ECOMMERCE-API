#!/bin/bash

# Apply database migrations
echo "Apply database migrations"
python manage.py migrate

# Collect static files
echo "Collect static files"
python manage.py collectstatic --no-input

# Start server
echo "Starting server"
gunicorn eccomerce_api.wsgi:application --bind 0.0.0.0:8000