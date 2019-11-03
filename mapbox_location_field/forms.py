from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

from .widgets import MapInput, AddressAutoHiddenInput


def parse_location(location_string):
    """parse and convert coordinates from string to tuple"""

    args = location_string.split(",")
    if len(args) != 2:
        raise ValidationError(_("Invalid input for a Location instance"))

    lat = args[0]
    lng = args[1]

    try:
        lat = float(lat)
    except ValueError:
        raise ValidationError(_("Invalid input for a Location instance. Latitude must be convertible to float "))
    try:
        lng = float(lng)
    except ValueError:
        raise ValidationError(_("Invalid input for a Location instance. Longitude must be convertible to float "))

    return lat, lng


class LocationField(forms.CharField):
    """custom form field for picking location"""

    def __init__(self, *args, **kwargs):
        map_attrs = kwargs.pop("map_attrs", None)
        self.widget = MapInput(map_attrs=map_attrs, )

        super().__init__(*args, **kwargs)
        self.error_messages = {"required": "Please pick a location, it's required", }


class AddressAutoHiddenField(forms.CharField):
    """custom form field which uses AddressAutoHiddenInput"""
    widget = AddressAutoHiddenInput()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.label = ""


