"""
Configuration pour pytest.
"""

import os
import django
import pytest
from django.db import connections

# Configurez Django avant d'exécuter les tests
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "oc_lettings_site.settings")
django.setup()


@pytest.fixture(autouse=True)
def enable_db_access_for_all_tests(db):
    """
    Permet à tous les tests d'accéder à la base de données sans avoir à spécifier
    explicitement la fixture db.
    
    Cela résout les problèmes "Cannot operate on a closed database" qui peuvent
    survenir lors de l'exécution des tests.
    """
    # Cette fixture ne fait rien, mais elle force l'utilisation de la fixture db
    # qui configure une base de données de test pour chaque test
    pass


@pytest.fixture(autouse=True)
def close_all_connections():
    """
    Ferme toutes les connexions après chaque test pour éviter les erreurs
    "Cannot operate on a closed database".
    """
    yield
    # Ferme les connexions après chaque test
    for conn in connections.all():
        conn.close()
