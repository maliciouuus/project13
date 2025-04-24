#!/bin/bash
set -e

# Désactiver Sentry pour le test
export SENTRY_DSN=""

# Créer le répertoire de logs
mkdir -p /app/logs

# Migrations
echo "Applying migrations..."
python manage.py migrate

# Create admin user
echo "Creating admin user..."
python manage.py create_superuser

# Start server
echo "Starting server..."
exec gunicorn oc_lettings_site.wsgi:application --bind 0.0.0.0:8000 --workers 2 