from django.contrib.gis.geos import Point
from django.test import TestCase

from mapbox_location_field.forms import LocationField, AddressAutoHiddenField
from mapbox_location_field.spatial.forms import SpatialLocationField
from mapbox_location_field.widgets import MapInput, AddressAutoHiddenInput, reverse_tuple_string


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

    def test_clean(self):
        field = LocationField()
        self.assertEqual("12, 11", field.clean("12, 11"))


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
        point = field.clean("12,13")

        self.assertIsInstance(point, Point)
        self.assertEqual(point.x, 12)
        self.assertEqual(point.y, 13)

        point = field.clean("12")
        self.assertIsNone(point)

    def test_to_python(self):
        field = SpatialLocationField()

        for empty in field.empty_values:
            self.assertIsNone(field.to_python(empty))

        point = Point(12, 13)
        self.assertIs(point, field.to_python(point))

        point = field.to_python("12,13")
        self.assertIsInstance(point, Point)
        self.assertEqual(point.x, 12)
        self.assertEqual(point.y, 13)

    def test_reverse_tuple_string(self):
        self.assertEqual(reverse_tuple_string("1,2"), "2,1")

    def test_empty_reverse_tuple_string(self):
        self.assertEqual(reverse_tuple_string(""), "")


class AddressAutoHiddenFieldTests(TestCase):
    def test_widget(self):
        field = AddressAutoHiddenField()
        self.assertEqual(field.widget.__class__, AddressAutoHiddenInput().__class__)

    def test_label(self):
        field = AddressAutoHiddenField()
        self.assertEqual(field.label, "")

    def test_passing_map_id(self):
        field = AddressAutoHiddenField(map_id="test_map_id")
        self.assertEqual(field.widget.map_id, "test_map_id")
