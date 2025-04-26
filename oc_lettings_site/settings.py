import os
import sentry_sdk
from dotenv import load_dotenv
from pathlib import Path
from sentry_sdk.integrations.django import DjangoIntegration
import sys

# -------------------------------------------------------------------------
# MODIFICATION: Utilisation de python-dotenv pour charger les variables d'environnement
# d'un fichier .env, ce qui facilite la configuration dans différents environnements
# sans exposer de données sensibles dans le code source.
# -------------------------------------------------------------------------
# Load environment variables from .env file
load_dotenv()

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# -------------------------------------------------------------------------
# MODIFICATION: Utilisation d'une variable d'environnement pour la clé secrète,
# avec une valeur par défaut pour le développement local. Dans un environnement
# de production, cette clé devrait être définie via la variable d'environnement.
# -------------------------------------------------------------------------
# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv(
    "DJANGO_SECRET_KEY", "fp$9^593hsriajg$_%=5trot9g!1qa@ew(o-1#@=&4%=hp46(s"
)

# -------------------------------------------------------------------------
# MODIFICATION: Configuration flexible du mode DEBUG via une variable d'environnement.
# La conversion str -> bool est gérée par la comparaison avec "true" en minuscules.
# -------------------------------------------------------------------------
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv("DEBUG", "True").lower() == "true"

# -------------------------------------------------------------------------
# MODIFICATION: Configuration des hôtes autorisés via variables d'environnement.
# Pour la production, définir ALLOWED_HOSTS comme une liste séparée par virgules.
# -------------------------------------------------------------------------
# Get the allowed hosts from environment variables
allowed_hosts_env = os.getenv("ALLOWED_HOSTS", "")
if allowed_hosts_env:
    ALLOWED_HOSTS = allowed_hosts_env.split(",")
else:
    ALLOWED_HOSTS = [
        ".localhost",
        "127.0.0.1",
        "127.0.0.1:8000",
        "[::1]",
        "0.0.0.0",
        "testserver",
    ]

# Always include testserver for testing
if "testserver" not in ALLOWED_HOSTS:
    ALLOWED_HOSTS.append("testserver")

# Montrer les détails des exceptions seulement en mode DEBUG
DEBUG_PROPAGATE_EXCEPTIONS = DEBUG

# -------------------------------------------------------------------------
# MODIFICATION: Configuration de Sentry pour le suivi des erreurs en production.
# Sentry n'est initialisé que si la variable d'environnement SENTRY_DSN est définie.
# -------------------------------------------------------------------------
# Sentry configuration - only initialize if DSN is provided
sentry_dsn = os.getenv("SENTRY_DSN")
if sentry_dsn:
    sentry_sdk.init(
        dsn=sentry_dsn,
        integrations=[DjangoIntegration()],
        traces_sample_rate=float(os.getenv("SENTRY_TRACES_SAMPLE_RATE", "1.0")),
        environment=os.getenv("SENTRY_ENVIRONMENT", "development"),
        send_default_pii=True,
    )

# -------------------------------------------------------------------------
# MODIFICATION: Création automatique du répertoire de logs pour stocker les journaux.
# -------------------------------------------------------------------------
# Create logs directory if it doesn't exist
logs_dir = os.path.join(BASE_DIR, "logs")
os.makedirs(logs_dir, exist_ok=True)

# -------------------------------------------------------------------------
# MODIFICATION: Configuration avancée de journalisation avec plusieurs handlers
# (console, fichier) et formatters pour différents niveaux de détail.
# Chaque application a son propre logger configuré.
# -------------------------------------------------------------------------
# Logging configuration
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "{levelname} {asctime} {module} {process:d} {thread:d} {message}",
            "style": "{",
        },
        "simple": {
            "format": "{levelname} {message}",
            "style": "{",
        },
    },
    "filters": {
        "require_debug_true": {
            "()": "django.utils.log.RequireDebugTrue",
        },
    },
    "handlers": {
        "console": {
            "level": "INFO",
            "filters": ["require_debug_true"],
            "class": "logging.StreamHandler",
            "formatter": "simple",
        },
        "file": {
            "level": "WARNING",
            "class": "logging.FileHandler",
            "filename": os.path.join(logs_dir, "django.log"),
            "formatter": "verbose",
        },
    },
    "root": {
        "handlers": ["console", "file"],
        "level": "INFO",
    },
    "loggers": {
        "django": {
            "handlers": ["console", "file"],
            "level": "INFO",
            "propagate": True,
        },
        "oc_lettings_site": {
            "handlers": ["console", "file"],
            "level": "INFO",
            "propagate": True,
        },
        "lettings": {
            "handlers": ["console", "file"],
            "level": "INFO",
            "propagate": True,
        },
        "profiles": {
            "handlers": ["console", "file"],
            "level": "INFO",
            "propagate": True,
        },
    },
}


# -------------------------------------------------------------------------
# MODIFICATION: Configuration des applications installées avec nos nouvelles
# applications 'lettings' et 'profiles' ajoutées à la liste.
# -------------------------------------------------------------------------
# Application definition
INSTALLED_APPS = [
    "oc_lettings_site.apps.OCLettingsSiteConfig",
    "lettings.apps.LettingsConfig",
    "profiles.apps.ProfilesConfig",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# -------------------------------------------------------------------------
# MODIFICATION: Configuration conditionnelle de Whitenoise pour servir les fichiers
# statiques efficacement en production. Activé uniquement si USE_WHITENOISE=True
# dans les variables d'environnement. Si non activé, utilisation du stockage Django par défaut.
# -------------------------------------------------------------------------
# Add whitenoise middleware if environment variable is set
if os.getenv("USE_WHITENOISE", "False").lower() == "true":
    MIDDLEWARE.insert(1, "whitenoise.middleware.WhiteNoiseMiddleware")
    STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"
else:
    # Use the default Django static files storage when not using WhiteNoise
    STATICFILES_STORAGE = "django.contrib.staticfiles.storage.StaticFilesStorage"

ROOT_URLCONF = "oc_lettings_site.urls"

# -------------------------------------------------------------------------
# MODIFICATION: Configuration des templates avec un répertoire global 'templates'
# pour les templates partagés, en plus des templates spécifiques des applications.
# -------------------------------------------------------------------------
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "oc_lettings_site.wsgi.application"


# -------------------------------------------------------------------------
# MODIFICATION: Configuration de la base de données avec SQLite par défaut.
# Support pour PostgreSQL via dj_database_url si DATABASE_URL est configuré.
# -------------------------------------------------------------------------
# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases
# Use DATABASE_URL if provided, otherwise use SQLite
if 'pytest' in sys.modules:
    # Configuration de base de données en mémoire pour les tests
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': ':memory:',
        }
    }
else:
    # Configuration normale pour le développement et la production
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": os.path.join(BASE_DIR, "oc-lettings-site.sqlite3"),
        }
    }

# Use dj_database_url for PostgreSQL if available and DATABASE_URL is set
database_url = os.getenv("DATABASE_URL")
if database_url and "dj_database_url" in globals():
    import dj_database_url

    DATABASES["default"] = dj_database_url.config(
        default=database_url, conn_max_age=600
    )


# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")

STATIC_URL = "/static/"
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
]
