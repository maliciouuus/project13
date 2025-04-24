from django.db import models
from django.core.validators import MaxValueValidator, MinLengthValidator


# -------------------------------------------------------------------------
# MODIFICATION: Ce modèle était à l'origine dans oc_lettings_site/models.py
# Il a été déplacé vers sa propre application 'lettings' pour une meilleure
# organisation du code et une architecture plus modulaire
# -------------------------------------------------------------------------
class Address(models.Model):
    """
    Represents a physical address.
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
        Meta class for Address model
        """

        verbose_name_plural = "Addresses"


# -------------------------------------------------------------------------
# MODIFICATION: Ce modèle était à l'origine dans oc_lettings_site/models.py
# Il a été déplacé vers sa propre application 'lettings' pour une meilleure
# organisation du code et une architecture plus modulaire
# -------------------------------------------------------------------------
class Letting(models.Model):
    """
    Represents a property letting, linked to a physical address.
    """

    title = models.CharField(max_length=256)
    address = models.OneToOneField(Address, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
