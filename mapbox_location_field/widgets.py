from django.forms.widgets import HiddenInput
from django.utils.html import mark_safe

class MapInput(HiddenInput):
    class Media:
        js = ("js\map_input.js",)
        css = {
            "all": ("css\map_input.css",)
        }

    def render(self, name, value, attrs=None, renderer=None):
        rendered_html = super().render(name, value, attrs, renderer)
        rendered_html += "<div id='secret-id-map-mapbox-location-field' class='location-field-map'></div><div id='secret-id-geocoder-mapbox-location-field' class='location-field-geocoder'></div>"
        return mark_safe(rendered_html)

