from django.contrib.gis.forms import PointField, ValidationError
from django.contrib.gis.geos import Point

from ..forms import parse_location
from ..widgets import MapInput


class SpatialLocationField(PointField):
    """custom form field for picking location for spatial databases"""

    def __init__(self, *args, **kwargs):
        map_attrs = kwargs.pop("map_attrs", None)
        super(SpatialLocationField, self).__init__(*args, **kwargs)

        self.widget = MapInput(map_attrs=map_attrs, )
        self.error_messages = {"required": "Please pick a location, it's required", }

    def clean(self, value):
        try:
            return super(SpatialLocationField, self).clean(value)
        except (ValueError, ValidationError):
            return None

    def to_python(self, value):
        """Transform the value to a Geometry object."""
        if value in self.empty_values:
            return None

        if isinstance(value, Point):
            return value

        return Point(parse_location(value), srid=4326)
