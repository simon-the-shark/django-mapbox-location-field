from django.core.exceptions import ValidationError
from django.test import TestCase

from mapbox_location_field.forms import AddressAutoHiddenField as FormAddressAutoHiddenField
from mapbox_location_field.forms import LocationField as FormLocationField
from mapbox_location_field.models import parse_location, LocationField, AddressAutoHiddenField
from mapbox_location_field.spatial.forms import SpatialLocationField as FormSpatialLocationField
from mapbox_location_field.spatial.models import SpatialLocationField


class LocationFieldTests(TestCase):

    def assertRaisesValidationError(self, func, *args, **kwargs):
        with self.assertRaises(ValidationError):
            func(*args, **kwargs)

    def test_parse_location(self):
        self.assertEqual(parse_location("1,7"), (1, 7))
        self.assertEqual(parse_location("0.5542434352,7.14325463435626543674375"),
                         (0.5542434352, 7.14325463435626543674375))

        self.assertEqual(parse_location("1,7", "lat"), (7, 1))
        self.assertEqual(parse_location("0.5542434352,7.14325463435626543674375", "lat"),
                         (7.14325463435626543674375, 0.5542434352))

        self.assertRaisesValidationError(parse_location, "1,2,4,7,6")
        self.assertRaisesValidationError(parse_location, "1")
        self.assertRaisesValidationError(parse_location, "1,xD")
        self.assertRaisesValidationError(parse_location, "xD,1")
        self.assertRaisesValidationError(parse_location, "1,2", "alfhjksd")

    def test_LocationField(self):
        instance = LocationField()
        self.assertIsInstance(instance, LocationField)
        name, path, args, kwargs = instance.deconstruct()
        new_instance = LocationField(*args, **kwargs)
        self.assertEqual(instance.map_attrs, new_instance.map_attrs)

    def test_from_db_value(self):
        instance = LocationField()
        self.assertIsNone(instance.from_db_value(None))
        self.assertEqual(instance.from_db_value("1,1"), parse_location("1,1"))  # already tested above

    def test_to_python(self):
        instance = LocationField()
        self.assertIsNone(instance.to_python(None))
        self.assertEqual(instance.to_python((1, 2)), (1, 2))
        self.assertEqual(instance.to_python("1,1"), parse_location("1,1"))  # already tested above

    def test_get_prep_value(self):
        instance = LocationField()
        self.assertEqual("1,5", instance.get_prep_value((1, 5)))
        self.assertEqual(None, instance.get_prep_value(None))

    def test_form_field(self):
        instance = LocationField()
        self.assertTrue(isinstance(instance.formfield(), FormLocationField))

    def test_save_string(self):
        instance = LocationField()
        self.assertEqual("117, 112", instance.save_string("117, 112"))
        self.assertEqual("117,112", instance.save_string("117,112"))
        self.assertEqual("0,0", instance.save_string("45678"))

    def test_save_string_nullable(self):
        instance = LocationField(null=True)
        self.assertEqual("117, 112", instance.save_string("117, 112"))
        self.assertEqual("117,112", instance.save_string("117,112"))
        self.assertIsNone(instance.save_string("8346"))


class SpatialLocationFieldTests(TestCase):

    def test_SpatialLocationField(self):
        instance = SpatialLocationField()
        self.assertIsInstance(instance, SpatialLocationField)
        name, path, args, kwargs = instance.deconstruct()
        new_instance = SpatialLocationField(*args, **kwargs)
        self.assertEqual(instance.map_attrs, new_instance.map_attrs)

    def test_form_field(self):
        instance = SpatialLocationField()
        self.assertTrue(isinstance(instance.formfield(), FormSpatialLocationField))


class AddressAutoHiddenFieldTests(TestCase):
    def test_field(self):
        instance = AddressAutoHiddenField()
        self.assertIsInstance(instance, AddressAutoHiddenField)
        name, path, args, kwargs = instance.deconstruct()
        new_instance = AddressAutoHiddenField(*args, **kwargs)
        self.assertEqual(instance.map_id, new_instance.map_id)

    def test_form_field(self):
        instance = AddressAutoHiddenField()
        self.assertTrue(isinstance(instance.formfield(), FormAddressAutoHiddenField))
