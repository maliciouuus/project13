from django.shortcuts import render
from django.http import Http404, HttpResponseServerError
from .models import Letting
from oc_lettings_site.utils.logging_utils import log_info, log_error, log_function_call


@log_function_call
def index(request):
    """
    Affiche la liste de toutes les locations immobilières.

    Cette vue récupère toutes les locations depuis la base de données
    et les passe au template pour l'affichage.

    Args:
        request: La requête HTTP

    Returns:
        Template rendu avec la liste de toutes les locations
    """
    log_info("Fetching all lettings for index page")
    lettings_list = Letting.objects.all()
    context = {"lettings_list": lettings_list}
    return render(request, "lettings/index.html", context)


@log_function_call
def letting(request, letting_id):
    """
    Affiche les détails d'une location immobilière spécifique.

    Vérifie explicitement si la location existe et génère une erreur 404
    appropriée si elle n'existe pas.

    Args:
        request: La requête HTTP
        letting_id: ID de la location à afficher

    Returns:
        Template rendu avec les détails de la location

    Raises:
        Http404: Si la location n'existe pas
    """
    log_info(f"Fetching letting details for ID: {letting_id}")

    try:
        try:
            letting = Letting.objects.get(id=letting_id)
        except Letting.DoesNotExist:
            log_error(f"Letting with ID {letting_id} not found")
            raise Http404(f"Letting with ID {letting_id} does not exist")

        context = {
            "title": letting.title,
            "address": letting.address,
        }
        return render(request, "lettings/letting.html", context)
    except Http404:
        raise
    except Exception as e:
        log_error(f"Error retrieving letting with ID {letting_id}", exc_info=e)
        return HttpResponseServerError(render(request, "500.html"))
