from django.apps import AppConfig


class LettingsConfig(AppConfig):
    """
    Configuration de l'application lettings.
    Gère les paramètres spécifiques à l'application des locations.
    """

    default_auto_field = "django.db.models.BigAutoField"
    name = "lettings"
