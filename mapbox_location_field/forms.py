from django import forms

from .widgets import MapInput, AddressAutoHiddenInput


class LocationField(forms.CharField):
    """custom form field for picking location"""

    def __init__(self, *args, **kwargs):
        map_attrs = kwargs.pop("map_attrs", None)
        self.widget = MapInput(map_attrs=map_attrs, )

        super().__init__(*args, **kwargs)
        self.error_messages = {"required": "Please pick a location, it's required", }


class AddressAutoHiddenField(forms.CharField):
    widget = AddressAutoHiddenInput()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.label = ""
