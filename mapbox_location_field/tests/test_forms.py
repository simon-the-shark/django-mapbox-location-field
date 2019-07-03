from django.test import TestCase

from mapbox_location_field.forms import LocationField
from mapbox_location_field.widgets import MapInput


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
