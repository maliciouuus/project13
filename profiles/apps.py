from django.apps import AppConfig


class ProfilesConfig(AppConfig):
    """
    Configuration de l'application profiles.
    Gère les paramètres spécifiques à l'application des profils utilisateurs.
    """

    default_auto_field = "django.db.models.BigAutoField"
    name = "profiles"
