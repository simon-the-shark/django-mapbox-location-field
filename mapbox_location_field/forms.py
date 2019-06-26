from django import forms

from .widgets import MapInput


class LocationField(forms.CharField):
    widget = MapInput()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.error_messages = {"required": "Please pick a location, it's required", }
