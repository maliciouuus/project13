"""
Configuration pour pytest.
"""

import os
import django

# Configurez Django avant d'exécuter les tests
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "oc_lettings_site.settings")
django.setup()
