from django.conf import settings
from django.test import TestCase

from mapbox_location_field.widgets import MapInput, parse_tuple_string, AddressAutoHiddenInput, MapAdminInput, \
    AddressHiddenAdminInput


class MapInputTests(TestCase):
    def test_map_attrs_defaults(self):
        widget = MapInput()
        self.assertEqual(widget.map_attrs, {})
        self.assertEqual(widget.placeholder, "Pick a location on map below")
        self.assertTrue(widget.readonly)

    def test_map_attrs_customized(self):
        widget = MapInput(map_attrs={"readonly": False, "placeholder": "location", "zoom": 14})
        self.assertEqual(widget.map_attrs, {"zoom": 14, })
        self.assertEqual(widget.placeholder, "location")
        self.assertFalse(widget.readonly)

    def test_get_contex(self):
        widget = MapInput(map_attrs={"readonly": False, "placeholder": "cool location field placeholder"})
        contex = widget.get_context("location_field", None,
                                    {"placeholder": "not cool location field placeholder", "readonly": True, })

        self.assertEqual(contex["widget"]["attrs"]["placeholder"], "cool location field placeholder")
        self.assertFalse(contex["widget"]["attrs"]["readonly"])
        self.assertTrue(contex["widget"]["attrs"]["class"].endswith(" js-mapbox-input-location-field"))

    def test_get_contex_when_map_attrs_None(self):
        widget = MapInput()
        contex = widget.get_context("location_field", None, None)
        self.assertEqual(contex["widget"]["attrs"]["placeholder"], "Pick a location on map below")
        self.assertTrue(contex["widget"]["attrs"]["readonly"])
        self.assertTrue(contex["widget"]["attrs"]["class"].endswith(" js-mapbox-input-location-field"))

    def test_get_config_settings_defaults(self):
        widget = MapInput()
        settings.MAPBOX_KEY = "MY_COOL_MAPBOX_KEY"

        expected_map_attrs = {
            "style": "mapbox://styles/mapbox/outdoors-v11",
            "zoom": 13,
            "center": [17.031645, 51.106715],
            "cursor_style": 'pointer',
            "marker_color": "red",
            "rotate": False,
            "geocoder": True,
            "fullscreen_button": True,
            "navigation_buttons": True,
            "track_location_button": True,
            "id": "map"
        }
        result = widget.get_config_settings()
        self.assertEqual(result, expected_map_attrs)

    def test_get_config_settings_updated_with_map_attrs(self):
        expected_map_attrs = {
            "style": "cool style",
            "zoom": 90,
            "center": [1, 5.1],
            "cursor_style": 'cell',
            "marker_color": "blue",
            "rotate": True,
            "geocoder": False,
            "fullscreen_button": False,
            "navigation_buttons": False,
            "track_location_button": False,
            "id": "test_map_id"
        }

        widget = MapInput(map_attrs=expected_map_attrs)
        result = widget.get_config_settings()
        for key in expected_map_attrs.keys():
            self.assertEqual(result[key], expected_map_attrs[key])

    def test_parse_tuple_string(self):
        self.assertEqual(parse_tuple_string("(123456, 155413)"), (123456, 155413))
        self.assertEqual(parse_tuple_string("(123456.864534, 155413452)"), (123456.864534, 155413452))
        self.assertEqual(parse_tuple_string("(123456, 155413.452)"), (123456, 155413.452))
        self.assertEqual(parse_tuple_string("(123.456, 155413.452)"), (123.456, 155413.452))

        self.assertEqual(parse_tuple_string("(123456,155413)"), (123456, 155413))
        self.assertEqual(parse_tuple_string("(123456.864534,155413452)"), (123456.864534, 155413452))
        self.assertEqual(parse_tuple_string("(123456,155413.452)"), (123456, 155413.452))
        self.assertEqual(parse_tuple_string("(123.456,155413.452)"), (123.456, 155413.452))

        self.assertEqual(parse_tuple_string("SRID=4376POINT (123456 155413)"), (123456, 155413))
        self.assertEqual(parse_tuple_string("SRID=4376POINT (123456.864534 155413452)"), (123456.864534, 155413452))
        self.assertEqual(parse_tuple_string("SRID=4376POINT (123456 155413.452)"), (123456, 155413.452))
        self.assertEqual(parse_tuple_string("SRID=4376POINT (123.456 155413.452)"), (123.456, 155413.452))

    def test_setting_center_point(self):
        widget = MapInput()
        widget.get_context("name", (1234.3, 2352145.6), {})
        self.assertEqual(widget.center_point, '(1234.3, 2352145.6)')


class AddressAutoHiddenInputTests(TestCase):
    def test_get_context_when_map_attrs_None(self):
        widget = AddressAutoHiddenInput()
        contex = widget.get_context("addres_field", None, None)
        self.assertTrue(contex["widget"]["attrs"]["class"].endswith(" js-mapbox-address-input-location-field"))

    def test_get_context(self):
        widget = AddressAutoHiddenInput(map_id="test_map_id")
        context = widget.get_context("address_field", None, None)
        self.assertEqual(context["map_id"], "test_map_id")


class AdminWidgetsTests(TestCase):
    def test_map_widget_media(self):
        widget = MapAdminInput()
        media = widget.media
        self.assertEqual(len(media._js), 0)

    def test_address_widget_media(self):
        widget = AddressHiddenAdminInput()
        media = widget.media
        self.assertEqual(len(media._js), 0)
