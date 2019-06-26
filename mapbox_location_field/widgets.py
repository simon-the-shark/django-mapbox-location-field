from django.forms.widgets import TextInput


class MapInput(TextInput):
    template_name = "mapbox_location_field\map_input.html"

    class Media:
        js = ("js\map_input.js",)
        css = {
            "all": ("css\map_input.css",)
        }

    def get_context(self, name, value, attrs):
        attrs.update({
            "class": "js-mapbox-input-location-field",
            "maxlenght": 63,
            "readonly": True,
            "placeholder": "Pick a location on map below"
        })

        return super().get_context(name, value, attrs)
