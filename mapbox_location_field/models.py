from __future__ import annotations

from django.db import models
from django.utils.translation import gettext_lazy as _

from .forms import AddressAutoHiddenField as AddressAutoHiddenFormField, parse_location, ValidationError
from .forms import LocationField as LocationFormField


class LocationField(models.CharField):
    """ custom model field for storing location """

    description = _("Location field (latitude and longitude).")

    def __init__(self, *args, **kwargs):
        kwargs["max_length"] = 63
        self.map_attrs = kwargs.pop("map_attrs", {})
        super(LocationField, self).__init__(*args, **kwargs)

    def deconstruct(self):
        name, path, args, kwargs = super(LocationField, self).deconstruct()
        del kwargs["max_length"]
        kwargs["map_attrs"] = self.map_attrs
        return name, path, args, kwargs

    def from_db_value(self, value: str | None, expression=None, connection=None):
        if not value:
            return value
        return parse_location(value)

    def to_python(self, value: tuple | None | str) -> tuple[float, float] | None:
        if isinstance(value, tuple):
            return value[0], value[1]
        elif not value:
            return value
        return parse_location(value)

    def get_prep_value(self, value: str | tuple[float, float] | None) -> str:
        if not value:
            return value

        if isinstance(value, str):
            return self.save_string(value)

        return "{},{}".format(value[0], value[1])

    def formfield(self, **kwargs):
        defaults = {'form_class': LocationFormField}
        defaults.update(kwargs)
        defaults.update({"map_attrs": self.map_attrs})
        return super(LocationField, self).formfield(**defaults)

    def value_to_string(self, obj):
        value = self.value_from_object(obj)
        return self.get_prep_value(value)

    def save_string(self, value: str) -> str | None:
        """ protect db from invalid string value """
        try:
            parse_location(value)
        except ValidationError:
            if self.null:
                return None
            else:
                return "0,0"
        return value


class AddressAutoHiddenField(models.TextField):
    """ custom model field for storing address """
    description = _("Address field which automatically fill with address from LocationField.")

    def __init__(self, *args, **kwargs):
        self.map_id = kwargs.pop("map_id", "map")
        super(AddressAutoHiddenField, self).__init__(*args, **kwargs)

    def deconstruct(self):
        name, path, args, kwargs = super(AddressAutoHiddenField, self).deconstruct()
        kwargs["map_id"] = self.map_id
        return name, path, args, kwargs

    def formfield(self, **kwargs):
        defaults = {'form_class': AddressAutoHiddenFormField}
        defaults.update(kwargs)
        defaults.update({"map_id": self.map_id})
        return models.Field.formfield(self, **defaults)
