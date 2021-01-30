from django.conf import settings
from django.forms import Media
from django.forms.widgets import TextInput


def parse_tuple_string(tuple_string):
    if "POINT" in tuple_string:
        list = tuple_string.split(" ")[1:]
        list[0] = list[0][1:]
        list[1] = list[1][:-1]
        return tuple(map(float, list))

    return tuple(map(float, tuple_string[1:-1].split(",")))


class MapInput(TextInput):
    """widget for picking your location"""

    template_name = "mapbox_location_field/map_input.html"

    def __init__(self, attrs=None, map_attrs=None):
        if map_attrs is None:
            map_attrs = {}
        self.map_attrs = map_attrs
        self.readonly = self.map_attrs.get("readonly", True)
        self.placeholder = self.map_attrs.get("placeholder", "Pick a location on map below")
        self.center_point = False

        super().__init__(attrs)

    class Media:
        js = ("mapbox_location_field/js/map_input.js",)
        css = {
            "all": ("mapbox_location_field/css/map_input.css",)
        }

    def get_context(self, name, value, attrs):
        if attrs is None:
            attrs = {}

        must_be_attrs = {
            "readonly": self.readonly,
            "placeholder": self.placeholder
        }
        attrs.update(must_be_attrs)
        attrs["class"] = attrs.get("class", "") + " js-mapbox-input-location-field"
        attrs["id"] = self.map_attrs.get("id", "map")

        context = super().get_context(name, value, attrs)
        self.center_point = context["widget"].get("value", False)
        context["key"] = settings.MAPBOX_KEY
        context["mapbox_attrs"] = self.get_config_settings()
        return context

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
            "id": "map"
        }

        if self.map_attrs is not None:
            default_map_attrs.update(self.map_attrs)

        if self.center_point:
            default_map_attrs["center"] = parse_tuple_string(self.center_point)

        return default_map_attrs


class AddressAutoHiddenInput(TextInput):
    """hidden text input which automatically fill itself with address from MapInput"""
    template_name = "mapbox_location_field/address_input.html"

    def __init__(self, attrs=None, map_id="map"):
        self.map_id = map_id
        super().__init__(attrs)
        self.label = ""

    def get_context(self, name, value, attrs):
        if attrs is None:
            attrs = {}
        attrs["class"] = attrs.get("class", "") + " js-mapbox-address-input-location-field"
        context = super().get_context(name, value, attrs)

        context["map_id"] = self.map_id
        return context

    class Media:
        js = ("mapbox_location_field/js/address_input.js",)
        css = {
            "all": ("mapbox_location_field/css/address_input.css",)
        }


class MapAdminInput(MapInput):
    """map input, but with javascript excluded from media"""

    @property
    def media(self):
        return Media(css={"all": ("mapbox_location_field/css/map_input.css",)})


class AddressHiddenAdminInput(AddressAutoHiddenInput):
    """address input, but with javascript excluded from media"""

    @property
    def media(self):
        return Media(css={"all": ("mapbox_location_field/css/address_input.css",)})
