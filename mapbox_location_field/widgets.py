from django.forms.widgets import TextInput
from django.conf import settings


class MapInput(TextInput):
    """widget for picking your location"""

    template_name = "mapbox_location_field\map_input.html"

    def __init__(self, attrs=None, map_attrs=None):
        self.map_attrs = map_attrs
        self.readonly = self.map_attrs.pop("readonly", True)
        self.placeholder = self.map_attrs.pop("placeholder", "Pick a location on map below")
        super().__init__(attrs)

    class Media:
        js = ("mapbox_location_field/js/map_input.js",)
        css = {
            "all": ("mapbox_location_field/css/map_input.css",)
        }

    def get_context(self, name, value, attrs):
        must_be_attrs = {
            "readonly": self.readonly,
            "placeholder": self.placeholder
        }

        attrs.update(must_be_attrs)
        attrs["class"] = attrs.get("class", "") + " js-mapbox-input-location-field"

        return super().get_context(name, value, attrs)

    def render(self, name, value, attrs=None, renderer=None):
        """attaches js config vars to rendered html"""
        rend = super().render(name, value, attrs, renderer)
        rend += self.get_config_settings()
        return rend

    def get_config_settings(self):
        """renders javascript configuration variables definitions"""
        default_map_attrs = {
            "style": "mapbox://styles/mapbox/outdoors-v11",
            "zoom": 13,
            "center": [17.031645, 51.106715],
            "cursor_style": 'pointer',
            "marker_color": "red",
            "rotate": False,
            "geocoder": True,
            "fullscreen_button": True,
            "navigation_buttons": True,
            "track_location_button": True,
        }
        if self.map_attrs is not None:
            default_map_attrs.update(self.map_attrs)
        js = "<script>mapboxgl.accessToken = '{}';{}</script>".format(settings.MAPBOX_KEY,
                                                                      self.map_attrs_to_javascript(default_map_attrs))
        return js

    @staticmethod
    def map_attrs_to_javascript(map_attrs):
        """renders javascript variables from dictionary of attrs"""
        js = ""
        js_pattern = "var map_attr_{key} = '{value}';"
        js_pattern_literally = "var map_attr_{key} = {value};"
        for key, value in map_attrs.items():
            if type(value) == list or type(value) == tuple:
                js += js_pattern_literally.format(key=key, value=list(value))
            elif type(value) == bool:
                val = str(value).lower()
                js += js_pattern_literally.format(key=key, value=val)
            else:
                js += js_pattern.format(key=key, value=value)
        return js


class MapAdminInput(MapInput):
    """map input, but with custom css and not defined in media js"""

    class Media:
        css = {
            "all": ("mapbox_location_field/css/map_input.css",)
        }
