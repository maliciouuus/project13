FROM python:3.9-slim

WORKDIR /app

# Installer les dépendances de base
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Variables d'environnement
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV DEBUG=False
ENV USE_WHITENOISE=True

# Copier les requirements et installer les dépendances
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Créer le répertoire pour les logs et staticfiles
RUN mkdir -p logs staticfiles

# Copier le code source
COPY . .

# Collect static files
# Using ignore errors to prevent build failures due to missing static files
RUN python manage.py collectstatic --noinput --clear || true

# Exécuter les migrations au démarrage et lancer le serveur
CMD sh -c "python manage.py migrate && gunicorn oc_lettings_site.wsgi:application --bind 0.0.0.0:8000"

# Exposer le port
EXPOSE 8000 