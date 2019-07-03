from django.test import TestCase
from django.conf import settings

from mapbox_location_field.widgets import MapInput


class MapInputTests(TestCase):

    def test_map_attrs_defaults(self):
        self.maxDiff = None

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

    def test_map_attrs_to_javascript(self):
        widget = MapInput()
        map_attrs = {
            "list": [1, 2],
            "tuple": (1, 2),
            "bool": True,
            "string": "cool string",
            "int": 1,
            "float": 1.2,
        }

        javascript = widget.map_attrs_to_javascript(map_attrs)
        expected_js = "var map_attr_list = [1, 2];var map_attr_tuple = [1, 2];var map_attr_bool = true;var map_attr_string = 'cool string';var map_attr_int = '1';var map_attr_float = '1.2';"
        self.assertEqual(expected_js, javascript)

    def test_get_config_settings_defaults(self):
        widget = MapInput()
        settings.MAPBOX_KEY = "MY_COOL_MAPBOX_KEY"
        javascript = widget.map_attrs_to_javascript({  # already tested above
            "style": "mapbox://styles/mapbox/outdoors-v11",
            "zoom": 13,
            "center": [17.031645, 51.106715],
            "cursor_style": 'pointer',
            "marker_color": "red",
            "rotate": False,
            "geocoder": True,
            "fullscreen_button": True,
            "navigation_buttons": True,
            "track_location_button": True, })

        expected_result = "<script>mapboxgl.accessToken = 'MY_COOL_MAPBOX_KEY';{}</script>".format(javascript)
        result = widget.get_config_settings()
        self.assertEqual(result, expected_result)

    def test_get_config_settings_defaults_updated_with_map_attrs(self):
        map_attrs = {
            "style": "cool style",
            "zoom": 90,
            "center": [1, 5.1],
            "cursor_style": 'cell',
            "marker_color": "blue",
            "rotate": True,
            "geocoder": False,
            "fullscreen_button": False,
            "navigation_buttons": False,
            "track_location_button": False, }

        widget = MapInput(map_attrs=map_attrs)
        settings.MAPBOX_KEY = "MY_COOL_MAPBOX_KEY"
        javascript = widget.map_attrs_to_javascript(map_attrs)  # already tested above

        expected_result = "<script>mapboxgl.accessToken = 'MY_COOL_MAPBOX_KEY';{}</script>".format(javascript)
        result = widget.get_config_settings()
        self.assertEqual(result, expected_result)

    def test_render(self):
        settings.MAPBOX_KEY = "MY_COOL_MAPBOX_KEY"
        widget = MapInput()
        expected_rend = '<input type="text" name="location" maxlength="63" class="form-group js-mapbox-input-location-field" required id="id_location" readonly placeholder="Pick a location on map below">\n\n' + "<div id='secret-id-map-mapbox-location-field' class='location-field-map'></div>\n<div id='secret-id-geocoder-mapbox-location-field' class='location-field-geocoder'></div><script>mapboxgl.accessToken = 'MY_COOL_MAPBOX_KEY';var map_attr_style = 'mapbox://styles/mapbox/outdoors-v11';var map_attr_zoom = '13';var map_attr_center = [17.031645, 51.106715];var map_attr_cursor_style = 'pointer';var map_attr_marker_color = 'red';var map_attr_rotate = false;var map_attr_geocoder = true;var map_attr_fullscreen_button = true;var map_attr_navigation_buttons = true;var map_attr_track_location_button = true;</script>"
        rend = widget.render("location", None,
                             attrs={"maxlength": 63, "class": "form-group", "required": True, "id": "id_location", })
        self.assertEqual(rend, expected_rend)
