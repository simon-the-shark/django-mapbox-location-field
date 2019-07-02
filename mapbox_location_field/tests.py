from django.test import TestCase
from django.core.exceptions import ValidationError

from .models import parse_location, LocationField


class LocationFieldTests(TestCase):

    def test_parse_location(self):
        self.assertEqual(parse_location("1,7"), (1, 7))
        self.assertEqual(parse_location("0.5542434352,7.14325463435626543674375"),
                         (0.5542434352, 7.14325463435626543674375))
        with self.assertRaises(ValidationError):
            parse_location("1,2,4,7,6")
        with self.assertRaises(ValidationError):
            parse_location("1")
        with self.assertRaises(ValidationError):
            parse_location("1,xD")
        with self.assertRaises(ValidationError):
            parse_location("xD,1")

    def test_LocationField(self):
        instance = LocationField()
        self.assertIsInstance(instance, LocationField)
        name, path, args, kwargs = instance.deconstruct()
        new_instance = LocationField(*args, **kwargs)
        self.assertEqual(instance.map_attrs, new_instance.map_attrs)

    def test_from_db_value(self):
        instance = LocationField()
        self.assertIsNone(instance.from_db_value(None))
        self.assertEqual(instance.from_db_value("1,1"), parse_location("1,1"))

    def test_to_python(self):
        instance = LocationField()
        self.assertIsNone(instance.to_python(None))
        self.assertEqual(instance.to_python((1, 2)), (1, 2))
        self.assertEqual(instance.to_python("1,1"), parse_location("1,1"))

    def test_get_prep_value(self):
        instance = LocationField()
        self.assertEqual("1,5", instance.get_prep_value((1, 5)))
