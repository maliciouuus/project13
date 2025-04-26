from django.db import models
from django.core.validators import MaxValueValidator, MinLengthValidator


# -------------------------------------------------------------------------
# MODIFICATION: Ce modèle était à l'origine dans oc_lettings_site/models.py
# Il a été déplacé vers sa propre application 'lettings' pour une meilleure
# organisation du code et une architecture plus modulaire.
#
# Cette migration a été réalisée via des fichiers de migration Django
# qui ont préservé les données existantes.
# -------------------------------------------------------------------------
class Address(models.Model):
    """
    Représente une adresse physique.

    Les validateurs garantissent l'intégrité des données:
    - 'number' doit être un entier positif inférieur à 10000
    - 'state' doit être exactement 2 caractères (code d'état US)
    - 'zip_code' doit être un entier positif à 5 chiffres max
    - 'country_iso_code' doit être au moins 3 caractères (ex: USA, FRA)
    """

    number = models.PositiveIntegerField(validators=[MaxValueValidator(9999)])
    street = models.CharField(max_length=64)
    city = models.CharField(max_length=64)
    state = models.CharField(max_length=2, validators=[MinLengthValidator(2)])
    zip_code = models.PositiveIntegerField(validators=[MaxValueValidator(99999)])
    country_iso_code = models.CharField(
        max_length=3, validators=[MinLengthValidator(3)]
    )

    def __str__(self):
        return f"{self.number} {self.street}, {self.city}, {self.state} {self.zip_code}"

    class Meta:
        """
        Meta classe pour le modèle Address

        MODIFICATION: Correction de la pluralisation pour afficher "Addresses"
        au lieu de "Addresss" dans l'interface d'administration
        """

        verbose_name_plural = "Addresses"


# -------------------------------------------------------------------------
# MODIFICATION: Ce modèle était à l'origine dans oc_lettings_site/models.py
# Il a été déplacé vers sa propre application 'lettings' pour une meilleure
# organisation du code et une architecture plus modulaire.
#
# La relation OneToOne avec Address est maintenue pour préserver
# l'intégrité référentielle de la base de données.
# -------------------------------------------------------------------------
class Letting(models.Model):
    """
    Représente une location immobilière, liée à une adresse physique.

    Chaque location est associée à une adresse unique (OneToOne).
    Si l'adresse est supprimée, la location sera également supprimée (CASCADE).
    """

    title = models.CharField(max_length=256)
    address = models.OneToOneField(Address, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
