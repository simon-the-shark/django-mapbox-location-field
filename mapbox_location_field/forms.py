from enum import Enum

from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from .widgets import MapInput, AddressAutoHiddenInput


class FirstInOrder(Enum):
    lng = "lng"
    lat = "lat"


def parse_location(location_string: str, first_in_order=FirstInOrder.lng) -> tuple[float, float]:
    """ parse and convert coordinates from string to tuple """

    args = location_string.split(",")
    if len(args) != 2:
        raise ValidationError(_("Invalid input for a Location instance"))

    if first_in_order == FirstInOrder.lat:
        lng = args[1]
        lat = args[0]
    elif first_in_order == FirstInOrder.lng:
        lng = args[0]
        lat = args[1]
    else:
        raise ValidationError(_("Invalid first letter for parsing location."))
    try:
        lat = float(lat)
    except ValueError:
        raise ValidationError(_("Invalid input for a Location instance. Latitude must be convertible to float "))
    try:
        lng = float(lng)
    except ValueError:
        raise ValidationError(_("Invalid input for a Location instance. Longitude must be convertible to float "))

    return lng, lat


class LocationField(forms.CharField):
    """ custom form field for picking location """

    def __init__(self, *args, **kwargs):
        map_attrs = kwargs.pop("map_attrs", None)
        super(LocationField, self).__init__(*args, **kwargs)

        self.widget = MapInput(map_attrs=map_attrs, )
        self.error_messages = {"required": "Please pick a location, it's required", }


class AddressAutoHiddenField(forms.CharField):
    """custom form field which uses AddressAutoHiddenInput"""
    widget = AddressAutoHiddenInput()

    def __init__(self, *args, **kwargs):
        map_id = kwargs.pop("map_id", "map")
        super(AddressAutoHiddenField, self).__init__(*args, **kwargs)

        self.widget = AddressAutoHiddenInput(map_id=map_id)
        self.label = ""
