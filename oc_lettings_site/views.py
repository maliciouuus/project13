from django.shortcuts import render

# MODIFICATION: Importation des utilitaires de journalisation personnalisés
from oc_lettings_site.utils.logging_utils import log_info, log_error, log_function_call


# MODIFICATION: Utilisation du décorateur pour journaliser les appels de fonction
@log_function_call
def index(request):
    """
    Displays the main homepage.

    Args:
        request: The HTTP request

    Returns:
        Rendered template with site index
    """
    # MODIFICATION: Journalisation de l'information
    log_info("Rendering homepage")
    return render(request, "index.html")


# MODIFICATION: Ajout d'un gestionnaire d'erreur 404 personnalisé
@log_function_call
def handler404(request, exception):
    """
    Handles 404 errors.

    Args:
        request: The HTTP request
        exception: The exception that was raised

    Returns:
        Rendered 404 template
    """
    # MODIFICATION: Journalisation de l'erreur avec l'exception
    log_error(f"404 error: {request.path}", exc_info=exception)
    return render(request, "404.html", status=404)


# MODIFICATION: Ajout d'un gestionnaire d'erreur 500 personnalisé
@log_function_call
def handler500(request):
    """
    Handles 500 errors.

    Args:
        request: The HTTP request

    Returns:
        Rendered 500 template
    """
    # MODIFICATION: Journalisation de l'erreur serveur
    log_error(f"500 error occurred while processing: {request.path}")
    return render(request, "500.html", status=500)


# MODIFICATION: Ajout d'une vue de test pour Sentry
@log_function_call
def sentry_test(request):
    """
    Test view to verify Sentry integration.

    Args:
        request: The HTTP request

    Raises:
        Exception: Always raises an exception to test Sentry error reporting
    """
    log_info("Testing Sentry integration")
    raise Exception(
        "This is a test exception to verify Sentry is capturing errors correctly."
    )


# MODIFICATION: Les vues ont été déplacées vers leurs applications respectives:
# - lettings_index and letting views are now in lettings.views
# - profiles_index and profile views are now in profiles.views
