from django.contrib import admin
from django.forms import Media

from .models import LocationField, AddressAutoHiddenField
from .widgets import MapAdminInput, AddressAutoHiddenInput


class MapAdmin(admin.ModelAdmin):
    """custom ModelAdmin for LocationField and AddressAutoHiddenField"""
    change_form_template = "mapbox_location_field/admin_change.html"
    formfield_overrides = {
        LocationField: {'widget': MapAdminInput},
        AddressAutoHiddenField: {"widget": AddressAutoHiddenInput, }

    }

    def change_view(self, request, object_id, form_url='', extra_context=None):
        """add map_input.js as separate argument in context"""
        extra_context = extra_context or {}
        extra_context["map_input_media"] = Media(js=("mapbox_location_field/js/map_input.js",))
        return super().change_view(request, object_id, form_url, extra_context=extra_context, )
