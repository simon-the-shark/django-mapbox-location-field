from __future__ import annotations

from django.conf import settings
from django.forms import Media
from django.forms.widgets import TextInput


def parse_tuple_string(tuple_string: str) -> tuple[float, float]:
    """ Parses a string to a tuple. Does not reverse any coords """
    if "POINT" in tuple_string:
        split = tuple_string.split(" ")[1:]
        return float(split[0][1:]), float(split[1][:-1])

    split = tuple_string.split(",")
    return float(split[0].strip(" ()")), float(split[1].strip(" ()"))


def reverse_tuple_string(location_string: str) -> str:
    if isinstance(location_string, str):
        if location_string == "":
            return location_string
        args = location_string.split(",")
        return args[1].strip() + "," + args[0].strip()
    else:
        return str(location_string[1]) + "," + str(location_string[0])


class MapInput(TextInput):
    """ widget for picking your location """

    template_name = "mapbox_location_field/map_input.html"

    def __init__(self, attrs=None, map_attrs=None):
        self.map_attrs = map_attrs or {}
        self.readonly = self.map_attrs.get("readonly", True)
        self.placeholder = self.map_attrs.get("placeholder", "Pick a location on map below")
        self.center_point = None
        super(MapInput, self).__init__(attrs)

    def format_value(self, value: str | None) -> str | None:
        if value == "" or value is None:
            return None
        return reverse_tuple_string(value)

    class Media:
        js = ("mapbox_location_field/js/map_input.js",)
        css = {
            "all": ("mapbox_location_field/css/map_input.css",)
        }

    def get_context(self, name, value, attrs):
        attrs = attrs or {}
        must_be_attrs = {
            "readonly": self.readonly,
            "placeholder": self.placeholder
        }
        attrs.update(must_be_attrs)

        attrs["class"] = attrs.get("class", "") + " js-mapbox-input-location-field"
        attrs["id"] = self.map_attrs.get("id", "map")

        context = super(MapInput, self).get_context(name, value, attrs)
        self.center_point = context["widget"].get("value", None)
        context["key"] = settings.MAPBOX_KEY
        context["mapbox_attrs"] = self.get_config_settings()
        return context

    def get_config_settings(self):
        """ renders javascript configuration variables definitions """
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
            "id": "map",
            "language": "auto",
            "message_404": "undefined address",
        }

        if self.map_attrs is not None:
            default_map_attrs.update(self.map_attrs)

        if self.center_point:
            default_map_attrs["center"] = parse_tuple_string(self.center_point)

        return default_map_attrs


class AddressAutoHiddenInput(TextInput):
    """ hidden text input which automatically fill itself with address from MapInput """
    template_name = "mapbox_location_field/address_input.html"

    def __init__(self, attrs=None, map_id="map"):
        self.map_id = map_id
        super(AddressAutoHiddenInput, self).__init__(attrs)
        self.label = ""

    def get_context(self, name, value, attrs):
        attrs = attrs or {}
        attrs["class"] = attrs.get("class", "") + " js-mapbox-address-input-location-field"

        context = super(AddressAutoHiddenInput, self).get_context(name, value, attrs)

        context["map_id"] = self.map_id
        return context

    class Media:
        js = ("mapbox_location_field/js/address_input.js",)
        css = {
            "all": ("mapbox_location_field/css/address_input.css",)
        }


class MapAdminInput(MapInput):
    """ map input, but with javascript excluded from media """

    @property
    def media(self):
        return Media(css={"all": ("mapbox_location_field/css/map_input.css",)})


class AddressHiddenAdminInput(AddressAutoHiddenInput):
    """ address input, but with javascript excluded from media """

    @property
    def media(self):
        return Media(css={"all": ("mapbox_location_field/css/address_input.css",)})
