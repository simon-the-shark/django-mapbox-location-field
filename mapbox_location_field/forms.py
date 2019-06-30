from django import forms

from .widgets import MapInput


class LocationField(forms.CharField):

    def __init__(self, *args, **kwargs):
        map_attrs = kwargs.pop("map_attrs", None)
        self.widget = MapInput(map_attrs=map_attrs,)

        super().__init__(*args, **kwargs)
        self.error_messages = {"required": "Please pick a location, it's required", }
