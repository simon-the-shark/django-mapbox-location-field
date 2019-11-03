from django.contrib.gis.db.models import PointField
from django.utils.translation import ugettext_lazy as _

from .forms import SpatialLocationField as SpatialLocationFormField


class SpatialLocationField(PointField):
    """custom model field for storing location in spatial databases"""

    description = _("Location field for spatial databases, stores Points.")

    def __init__(self, *args, **kwargs):
        self.map_attrs = kwargs.pop("map_attrs", {})
        super().__init__(*args, **kwargs)

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        kwargs["map_attrs"] = self.map_attrs
        return name, path, args, kwargs

    def formfield(self, **kwargs):
        defaults = {'form_class': SpatialLocationFormField}
        defaults.update(kwargs)
        defaults.update({"map_attrs": self.map_attrs})
        return super().formfield(**defaults)
