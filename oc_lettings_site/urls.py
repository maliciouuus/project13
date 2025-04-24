"""URLs de l'application principale."""

from django.contrib import admin
from django.urls import path, include

from . import views

# MODIFICATION: Ajout des gestionnaires d'erreurs personnalisés
# Ces gestionnaires affichent des pages d'erreur conviviales et enregistrent les erreurs
handler404 = "oc_lettings_site.views.handler404"
handler500 = "oc_lettings_site.views.handler500"

urlpatterns = [
    path("", views.index, name="index"),
    # MODIFICATION: Utilisation des espaces de noms pour les applications séparées
    path("lettings/", include("lettings.urls", namespace="lettings")),
    path("profiles/", include("profiles.urls", namespace="profiles")),
    path("admin/", admin.site.urls),
    # MODIFICATION: Ajout d'un point de terminaison pour tester l'intégration Sentry
    path("sentry-test/", views.sentry_test, name="sentry_test"),
]
