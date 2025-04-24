from django.contrib import admin
from .models import Profile


class ProfileAdmin(admin.ModelAdmin):
    """
    Admin configuration for Profile model.
    """

    list_display = ("user", "favorite_city")
    search_fields = ("user__username", "favorite_city")


admin.site.register(Profile, ProfileAdmin)
