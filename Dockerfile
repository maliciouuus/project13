FROM python:3.9-slim

WORKDIR /app

# Installer les dépendances de base
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    nginx \
    && rm -rf /var/lib/apt/lists/*

# Variables d'environnement
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV DEBUG=True
ENV USE_WHITENOISE=False

# Copier les requirements et installer les dépendances
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Créer le répertoire pour les logs et staticfiles
RUN mkdir -p logs staticfiles

# Copier le code source
COPY . .

# Collect static files with DEBUG=True and no compression
RUN python manage.py collectstatic --noinput --clear

# Configurer Nginx
RUN echo 'server {\n\
    listen 80;\n\
    server_name localhost;\n\
    location /static/ {\n\
        alias /app/staticfiles/;\n\
    }\n\
    location / {\n\
        proxy_pass http://127.0.0.1:8000;\n\
        proxy_set_header Host $host;\n\
        proxy_set_header X-Real-IP $remote_addr;\n\
    }\n\
}' > /etc/nginx/sites-available/default

# Créer un script d'entrée pour exécuter les migrations, créer le superutilisateur, et démarrer Gunicorn et Nginx
RUN echo '#!/bin/sh\n\
python manage.py migrate\n\
python manage.py create_superuser\n\
service nginx start\n\
gunicorn oc_lettings_site.wsgi:application --bind 127.0.0.1:8000 --workers 2 --log-level debug --access-logfile=-\n\
' > /app/docker-entrypoint.sh \
&& chmod +x /app/docker-entrypoint.sh

# Exécuter le script d'entrée au démarrage
CMD ["/app/docker-entrypoint.sh"]

# Exposer le port
EXPOSE 80 