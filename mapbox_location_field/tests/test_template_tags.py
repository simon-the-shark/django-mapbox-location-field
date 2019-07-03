from django.test import SimpleTestCase
from django.template import Template, Context


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

    def test_include_jquery(self):
        template_to_render = Template(
            "{% load mapbox_location_field_tags %}"
            "{% include_jquery %}"
        )
        rendered_template = template_to_render.render(Context())
        self.assertInHTML(
            "<script src='https://code.jquery.com/jquery-3.2.1.slim.min.js' integrity='sha384-KJ3o2DKtIkvYIK3UENzmM7KCkRr/rE9/Qpg6aAZGJwFDMVNA/GpGFF93hXpG5KkN' crossorigin='anonymous'></script>",
            rendered_template)
