from django.db import models
from django.contrib.auth.models import User


# -------------------------------------------------------------------------
# MODIFICATION: Ce modèle était à l'origine dans oc_lettings_site/models.py
# Il a été déplacé vers sa propre application 'profiles' pour une meilleure
# organisation du code et une architecture plus modulaire.
#
# Cette migration a été effectuée en préservant toutes les données existantes
# via les fichiers de migration Django (sans SQL direct).
# -------------------------------------------------------------------------
class Profile(models.Model):
    """
    Représente un profil utilisateur avec des informations supplémentaires.

    Chaque profil est lié à un utilisateur Django unique (OneToOne).
    Si l'utilisateur est supprimé, le profil sera également supprimé (CASCADE).

    Le champ 'favorite_city' est optionnel (blank=True) et permet aux
    utilisateurs d'indiquer leur ville préférée.
    """

    # Relation OneToOne avec le modèle User intégré de Django
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    favorite_city = models.CharField(max_length=64, blank=True)

    def __str__(self):
        return self.user.username
