from django.shortcuts import render, get_object_or_404
from .models import Letting
from oc_lettings_site.utils.logging_utils import log_info, log_error, log_function_call


@log_function_call
def index(request):
    """
    Displays the list of all property lettings.

    Args:
        request: The HTTP request

    Returns:
        Rendered template with list of all lettings
    """
    log_info("Fetching all lettings for index page")
    lettings_list = Letting.objects.all()
    context = {"lettings_list": lettings_list}
    return render(request, "lettings/index.html", context)


@log_function_call
def letting(request, letting_id):
    """
    Displays the details of a specific property letting.

    Args:
        request: The HTTP request
        letting_id: ID of the letting to display

    Returns:
        Rendered template with letting details
    """
    log_info(f"Fetching letting details for ID: {letting_id}")
    try:
        letting = get_object_or_404(Letting, id=letting_id)
        context = {
            "title": letting.title,
            "address": letting.address,
        }
        return render(request, "lettings/letting.html", context)
    except Exception as e:
        log_error(f"Error retrieving letting with ID {letting_id}", exc_info=e)
        raise
