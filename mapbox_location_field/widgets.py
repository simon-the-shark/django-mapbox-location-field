from django.forms.widgets import TextInput
from django.conf import settings


class MapInput(TextInput):
    template_name = "mapbox_location_field\map_input.html"

    class Media:
        js = ("js\map_input.js",)
        css = {
            "all": ("css\map_input.css",)
        }

    def get_context(self, name, value, attrs):
        must_be_attrs = {
            "maxlenght": 63,
            "readonly": True,
            "placeholder": "Pick a location on map below"
        }

        attrs.update(must_be_attrs)
        attrs["class"] = attrs.get("class", "") + " js-mapbox-input-location-field"

        return super().get_context(name, value, attrs)

    def render(self, name, value, attrs=None, renderer=None):
        rend = super().render(name, value, attrs, renderer)
        rend += self.get_config_settings()
        return rend

    @staticmethod
    def get_config_settings():
        return "<script>mapboxgl.accessToken = '{}';</script>".format(settings.MAPBOX_KEY)
