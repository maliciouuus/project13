import os

from django.core.wsgi import get_wsgi_application

# Check if running in production environment (Render sets this variable)
if os.environ.get("RENDER", False):
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "oc_lettings_site.settings_prod")
else:
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "oc_lettings_site.settings")

application = get_wsgi_application()
