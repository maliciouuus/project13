from django.db import models
from django.contrib.auth.models import User


# -------------------------------------------------------------------------
# MODIFICATION: Ce modèle était à l'origine dans oc_lettings_site/models.py
# Il a été déplacé vers sa propre application 'profiles' pour une meilleure
# organisation du code et une architecture plus modulaire
# -------------------------------------------------------------------------
class Profile(models.Model):
    """
    Represents a user profile with additional information.
    """

    # Champs conservés identiques au modèle d'origine
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    favorite_city = models.CharField(max_length=64, blank=True)

    def __str__(self):
        return self.user.username
