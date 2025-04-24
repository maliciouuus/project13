from django.shortcuts import render, get_object_or_404
from .models import Profile
from oc_lettings_site.utils.logging_utils import log_info, log_error, log_function_call


@log_function_call
def index(request):
    """
    Displays the list of all user profiles.

    Args:
        request: The HTTP request

    Returns:
        Rendered template with list of all profiles
    """
    log_info("Fetching all profiles for index page")
    profiles_list = Profile.objects.all()
    context = {"profiles_list": profiles_list}
    return render(request, "profiles/index.html", context)


@log_function_call
def profile(request, username):
    """
    Displays the details of a specific user profile.

    Args:
        request: The HTTP request
        username: Username of the profile to display

    Returns:
        Rendered template with profile details
    """
    log_info(f"Fetching profile details for username: {username}")
    try:
        user_profile = get_object_or_404(Profile, user__username=username)
        context = {"profile": user_profile}
        return render(request, "profiles/profile.html", context)
    except Exception as e:
        log_error(f"Error retrieving profile with username {username}", exc_info=e)
        raise
