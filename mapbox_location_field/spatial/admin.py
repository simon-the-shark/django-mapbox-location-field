from .models import SpatialLocationField

from ..admin import MapAdmin
from ..models import LocationField, AddressAutoHiddenField
from ..widgets import MapAdminInput, AddressHiddenAdminInput


class SpatialMapAdmin(MapAdmin):
    formfield_overrides = {
        LocationField: {'widget': MapAdminInput},
        SpatialLocationField: {'widget': MapAdminInput},
        AddressAutoHiddenField: {"widget": AddressHiddenAdminInput, }
    }
