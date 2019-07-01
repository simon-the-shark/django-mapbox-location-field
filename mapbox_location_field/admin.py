from django.contrib import admin
from django.forms import Media
from .widgets import MapAdminInput
from .models import LocationField


class MapAdmin(admin.ModelAdmin):
    change_form_template = "mapbox_location_field/admin_change.html"
    formfield_overrides = {
        LocationField: {'widget': MapAdminInput},
    }

    def change_view(self, request, object_id, form_url='', extra_context=None):
        extra_context = extra_context or {}
        extra_context["map_input_media"] = Media(js=("js/map_input.js",))
        return super().change_view(request, object_id, form_url, extra_context=extra_context, )
