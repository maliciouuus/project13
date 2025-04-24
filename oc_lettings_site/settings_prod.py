"""
Configuration Django pour l'environnement de production.
"""

import os
import dj_database_url
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

# Importer les paramètres de base
from .settings import *  # noqa

# Désactiver le mode DEBUG en production
DEBUG = False

# Configuration des hôtes autorisés
ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', '').split(',')

# Configuration de la base de données (PostgreSQL pour production)
DATABASE_URL = os.getenv('DATABASE_URL')
if DATABASE_URL:
    DATABASES = {
        'default': dj_database_url.config(default=DATABASE_URL, conn_max_age=600)
    }

# Configuration des fichiers statiques
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Ajouter whitenoise à la liste des middleware
if 'whitenoise.middleware.WhiteNoiseMiddleware' not in MIDDLEWARE:
    MIDDLEWARE.insert(1, 'whitenoise.middleware.WhiteNoiseMiddleware')

# Configuration de sécurité pour la production
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_HSTS_SECONDS = 31536000  # 1 an
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

# Configuration Sentry
sentry_sdk.init(
    dsn=os.getenv('SENTRY_DSN', ''),
    integrations=[DjangoIntegration()],
    traces_sample_rate=0.5,
    send_default_pii=True,
    environment="production",
)

# Configuration du logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}

