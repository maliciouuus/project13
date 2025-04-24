from django.contrib import admin
from .models import Letting, Address


class AddressAdmin(admin.ModelAdmin):
    """
    Admin configuration for Address model.
    """

    list_display = ("number", "street", "city", "state", "zip_code", "country_iso_code")
    search_fields = ("street", "city", "state")


class LettingAdmin(admin.ModelAdmin):
    """
    Admin configuration for Letting model.
    """

    list_display = ("title", "address")
    search_fields = ("title",)


admin.site.register(Letting, LettingAdmin)
admin.site.register(Address, AddressAdmin)
