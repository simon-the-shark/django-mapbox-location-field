from django.test import TestCase

from mapbox_location_field.forms import LocationField, AddressAutoHiddenField
from mapbox_location_field.widgets import MapInput, AddressAutoHiddenInput


class LocationFieldTests(TestCase):

    def test_widget(self):
        field = LocationField()
        self.assertEqual(field.widget.__class__, MapInput().__class__)

    def test_error_messages(self):
        field = LocationField()
        self.assertEqual(field.error_messages["required"], "Please pick a location, it's required")

    def test_passing_map_attrs(self):
        field = LocationField(map_attrs={"some": "value", "and some": "cool value"})
        self.assertEqual(field.widget.map_attrs, {"some": "value", "and some": "cool value"})


class AddressAutoHiddenFieldTests(TestCase):
    def test_widget(self):
        field = AddressAutoHiddenField()
        self.assertEqual(field.widget.__class__, AddressAutoHiddenInput().__class__)

    def test_label(self):
        field = AddressAutoHiddenField()
        self.assertEqual(field.label, "")
