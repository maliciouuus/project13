from django.shortcuts import render
from django.http import Http404
from .models import Profile
from oc_lettings_site.utils.logging_utils import (
    log_info, log_error, log_function_call
)


# MODIFICATION: Cette vue était à l'origine la fonction profiles_index
# dans oc_lettings_site/views.py. Elle a été déplacée et renommée en 'index'.
# Le décorateur log_function_call a été ajouté pour journaliser les appels.
@log_function_call
def index(request):
    """
    Affiche la liste de tous les profils utilisateurs.

    Cette vue récupère tous les profils depuis la base de données
    et les passe au template pour l'affichage.

    Args:
        request: La requête HTTP

    Returns:
        Template rendu avec la liste de tous les profils
    """
    # Journalisation pour le suivi des performances et le débogage
    log_info("Fetching all profiles for index page")

    # Récupération de tous les profils sans filtrage
    profiles_list = Profile.objects.all()
    context = {"profiles_list": profiles_list}

    # Le chemin du template a été modifié pour correspondre à la nouvelle structure d'application
    return render(request, "profiles/index.html", context)


# MODIFICATION: Cette vue était à l'origine la fonction profile dans oc_lettings_site/views.py
# Elle a été déplacée pour suivre l'architecture modulaire.
# La gestion d'erreur et la journalisation ont été améliorées.
@log_function_call
def profile(request, username):
    """
    Affiche les détails d'un profil utilisateur spécifique.

    Vérifie explicitement si le profil existe et génère une erreur 404
    appropriée si le profil demandé n'existe pas.

    Args:
        request: La requête HTTP
        username: Nom d'utilisateur du profil à afficher

    Returns:
        Template rendu avec les détails du profil

    Raises:
        Http404: Si le profil n'existe pas
    """
    # Journalisation pour le suivi des performances et le débogage
    log_info(f"Fetching profile details for username: {username}")

    try:
        # Vérification explicite si le profil existe, sinon lever Http404
        try:
            profile = Profile.objects.get(user__username=username)
        except Profile.DoesNotExist:
            log_error(f"Profile with username {username} not found")
            raise Http404(f"Profile with username {username} does not exist")

        # Si on arrive ici, le profil existe
        context = {"profile": profile}
        return render(request, "profiles/profile.html", context)
    except Http404:
        # Propager l'erreur Http404 pour qu'elle soit gérée par le handler404
        raise
    except Exception as e:
        # Journalisation structurée des erreurs pour faciliter le débogage
        log_error(f"Error retrieving profile with username {username}", exc_info=e)
        # Convertir l'erreur en Http500 pour utiliser notre template personnalisé
        from django.http import HttpResponseServerError
        return HttpResponseServerError(render(request, "500.html"))
