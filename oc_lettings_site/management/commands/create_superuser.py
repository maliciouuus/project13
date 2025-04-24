"""
Commande Django pour créer un superutilisateur admin par défaut si nécessaire.
"""

import logging
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User


class Command(BaseCommand):
    """
    Crée un superutilisateur 'admin' avec le mot de passe 'admin'
    s'il n'existe pas déjà.
    """

    help = "Crée un superutilisateur admin par défaut"

    def handle(self, *args, **options):
        try:
            if not User.objects.filter(username="admin").exists():
                User.objects.create_superuser(
                    username="admin", email="admin@example.com", password="admin"
                )
                self.stdout.write(
                    self.style.SUCCESS("✅ Superutilisateur 'admin' créé avec succès!")
                )
            else:
                self.stdout.write(
                    self.style.WARNING("⚠️  Le superutilisateur 'admin' existe déjà.")
                )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(
                    f"❌ Erreur lors de la création du superutilisateur: {str(e)}"
                )
            )
