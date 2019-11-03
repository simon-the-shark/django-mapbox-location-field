from django.contrib.gis.geos import Point
from django.test import TestCase

from mapbox_location_field.forms import LocationField, AddressAutoHiddenField, SpatialLocationField
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


class SpatialLocationFieldTests(TestCase):

    def test_widget(self):
        field = SpatialLocationField()
        self.assertEqual(field.widget.__class__, MapInput().__class__)

    def test_error_messages(self):
        field = SpatialLocationField()
        self.assertEqual(field.error_messages["required"], "Please pick a location, it's required")

    def test_passing_map_attrs(self):
        field = SpatialLocationField(map_attrs={"some": "value", "and some": "cool value"})
        self.assertEqual(field.widget.map_attrs, {"some": "value", "and some": "cool value"})

    def test_clean(self):
        field = SpatialLocationField()
        self.assertIsInstance(field.clean("12,12"), Point)


class AddressAutoHiddenFieldTests(TestCase):
    def test_widget(self):
        field = AddressAutoHiddenField()
        self.assertEqual(field.widget.__class__, AddressAutoHiddenInput().__class__)

    def test_label(self):
        field = AddressAutoHiddenField()
        self.assertEqual(field.label, "")
