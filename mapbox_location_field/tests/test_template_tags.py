from django.template import Template, Context
from django.test import SimpleTestCase

from mapbox_location_field.templatetags.mapbox_location_field_tags import tuple_to_array
from mapbox_location_field.templatetags.transform_map_attrs_to_js import transform_map_attrs_to_js


class TemplateTagsTest(SimpleTestCase):

    def test_location_field_includes(self):
        template_to_render = Template(
            "{% load mapbox_location_field_tags %}"
            "{% location_field_includes %}"
        )
        rendered_template = template_to_render.render(Context())
        self.assertInHTML(
            "<meta name='viewport' content='initial-scale=1,maximum-scale=1,user-scalable=no'/><script src='https://api.tiles.mapbox.com/mapbox-gl-js/v1.0.0/mapbox-gl.js'></script><link href='https://api.tiles.mapbox.com/mapbox-gl-js/v1.0.0/mapbox-gl.css' rel='stylesheet'/><script src='https://api.mapbox.com/mapbox-gl-js/plugins/mapbox-gl-geocoder/v4.4.0/mapbox-gl-geocoder.min.js'></script><link rel='stylesheet' href='https://api.mapbox.com/mapbox-gl-js/plugins/mapbox-gl-geocoder/v4.4.0/mapbox-gl-geocoder.css' type='text/css'/>",
            rendered_template)

    def test_include_jquery_full(self):
        template_to_render = Template(
            "{% load mapbox_location_field_tags %}"
            "{% include_jquery %}"
        )
        rendered_template = template_to_render.render(Context())
        self.assertInHTML(
            "<script src='https://code.jquery.com/jquery-3.3.1.min.js' integrity='sha384-tsQFqpEReu7ZLhBV2VZlAu7zcOV+rXbYlF2cqB8txI/8aZajjp4Bqd+V6D5IgvKT' crossorigin='anonymous' ></script>",
            rendered_template)


class TransformMapAttrsToJsTest(SimpleTestCase):
    def test_id_and_key(self):
        result = transform_map_attrs_to_js("test-id", "test_key", None)
        expected = "map_attrs['test-id'].test_key = "
        self.assertIn(expected, result)

    def test_list_input(self):
        result = transform_map_attrs_to_js("test-id", "test_key", [1, 2, 3])
        expected = "map_attrs['test-id'].test_key = [1, 2, 3];"
        self.assertEqual(expected, result)

    def test_tuple_input(self):
        result = transform_map_attrs_to_js("test-id", "test_key", (1, 2, 3))
        expected = "map_attrs['test-id'].test_key = [1, 2, 3];"
        self.assertEqual(expected, result)

    def test_true_input(self):
        result = transform_map_attrs_to_js("test-id", "test_key", True)
        expected = "map_attrs['test-id'].test_key = true;"
        self.assertEqual(expected, result)

    def test_false_input(self):
        result = transform_map_attrs_to_js("test-id", "test_key", False)
        expected = "map_attrs['test-id'].test_key = false;"
        self.assertEqual(expected, result)

    def test_string_input(self):
        result = transform_map_attrs_to_js("test-id", "test_key", "nice string for testing purposes")
        expected = "map_attrs['test-id'].test_key = 'nice string for testing purposes';"
        self.assertEqual(expected, result)

    def test_int_input(self):
        result = transform_map_attrs_to_js("test-id", "test_key", 5)
        expected = "map_attrs['test-id'].test_key = '5';"
        self.assertEqual(expected, result)

    def test_float_input(self):
        result = transform_map_attrs_to_js("test-id", "test_key", 5.9)
        expected = "map_attrs['test-id'].test_key = '5.9';"
        self.assertEqual(expected, result)


class TupleToArrayTest(SimpleTestCase):
    def test(self):
        self.assertEqual([12.0, 17.77], tuple_to_array((12.0, 17.77)))