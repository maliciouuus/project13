"""
Commande Django pour créer un superutilisateur par défaut si aucun n'existe.
Cette commande est utilisée principalement dans l'environnement Docker.
"""

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User


class Command(BaseCommand):
    """
    Commande Django pour créer un superutilisateur par défaut si aucun n'existe.
    Cette commande est utilisée principalement dans l'environnement Docker.
    """

    help = "Crée un superutilisateur par défaut (francis) si aucun utilisateur n'existe"

    def handle(self, *args, **options):
        if User.objects.count() == 0:
            username = "francis"
            password = "francis"
            email = "francis@example.com"

            self.stdout.write(f"Création du superutilisateur {username}")

            admin = User.objects.create_superuser(
                username=username, email=email, password=password
            )

            admin.save()

            self.stdout.write(
                self.style.SUCCESS(f"Superutilisateur {username} créé avec succès!")
            )
        else:
            self.stdout.write(
                "Un utilisateur existe déjà dans la base de données, aucun superutilisateur créé."
            )
