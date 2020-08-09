from django.contrib import admin
from django.forms import Media

from .models import LocationField, AddressAutoHiddenField
from .widgets import MapAdminInput, AddressHiddenAdminInput


class MapAdmin(admin.ModelAdmin):
    """custom ModelAdmin for LocationField and AddressAutoHiddenField"""
    change_form_template = "mapbox_location_field/admin_change.html"
    formfield_overrides = {
        LocationField: {'widget': MapAdminInput},
        AddressAutoHiddenField: {"widget": AddressHiddenAdminInput, }
    }

    def change_view(self, request, object_id, form_url='', extra_context=None):
        """add media that is placed below form as separate argument in context"""
        extra_context = extra_context or {}
        extra_context["bottom_media"] = Media(
            js=("mapbox_location_field/js/map_input.js", "mapbox_location_field/js/address_input.js"))
        return super().change_view(request, object_id, form_url, extra_context=extra_context, )

    def add_view(self, request, form_url='', extra_context=None):
        """add media that is placed below form as separate argument in context"""
        extra_context = extra_context or {}
        extra_context["bottom_media"] = Media(
            js=("mapbox_location_field/js/map_input.js", "mapbox_location_field/js/address_input.js"))
        return super().add_view(request, form_url, extra_context=extra_context, )
