
 # django-mapbox-location-field
 [![Build Status](https://travis-ci.org/Simon-the-Shark/django-mapbox-location-field.svg?branch=master)](https://travis-ci.org/Simon-the-Shark/django-mapbox-location-field) [![Coverage Status](https://coveralls.io/repos/github/Simon-the-Shark/django-mapbox-location-field/badge.svg?branch=master)](https://coveralls.io/github/Simon-the-Shark/django-mapbox-location-field?branch=master)
 ![PyPI](https://img.shields.io/pypi/v/django-mapbox-location-field.svg) ![PyPI - Downloads](https://img.shields.io/pypi/dm/django-mapbox-location-field)
 ****
 Simple in use **location model and form field** with **MapInput widget** for picking some location. Uses [mapbox gl js](https://docs.mapbox.com/mapbox-gl-js/), flexible map provider API. Fully compatible with bootstrap framework.
 ****
   
   
# Table of contents  
* [Why this?](#why-this)  
* [Live demo](#live-demo)  
* [Compatibility](#compatibility)  
* [Versions >1.4.0 note](#versions-140)  
* [Installation](#installation)  
* [Configuration](#configuration)  
* [Usage](#usage)  
  * [PLAIN (non-spatial) db](#plain-database)  
  * [SPATIAL db](#spatial-database)  
* [Customization](#customization)  
  * [map_attrs](#map_attrs)  
  * [bootstrap](#bootstrap)  
* [Admin interface usage](#admin-interface-usage)  
* [AddressAutoHiddenField](#addressautohiddenfield)  
* [Multiple fields usage](#multiple-fields-usage)  
* [Troubleshooting](#troubleshooting) 
* [Technologies](#technologies)  
  
# Why this?  
I was searching for some django location field which uses mapbox to use it in my project. However, I didn't find anything which suited my needs in 100% and that's why I created this simple django app. My philosophy was simplicity, but I wanted to create complete solution for picking location.  
  
Feel free to open issues, make pull request and request some features or instructions. Let me know if you think it is not flexible enough.  
# Live demo  
Curious how it works and looks like? See live demo on https://django-mapbox-location-field.herokuapp.com  
Demo app uses [django-bootstrap4](https://github.com/zostera/django-bootstrap4) for a little better looking form fields.  
You can also use it as a code example, because it is available on [my github](https://github.com/Simon-the-Shark/live_demo_django_mapbox_location_field).  
# Compatibility  
Automatically tested on Travis CI on versions:  
  
* Django 1.11, 2.0, 2.1, 2.2  
* Python 3.5, 3.6, 3.7  
  
PS. Django 1.11 does not support Python 3.7 anymore.  
  
#### Browser support  
django-mapbox-location-field support all browsers, which are supported by mapbox gl js. Read more [here](https://docs.mapbox.com/help/troubleshooting/mapbox-browser-support/#mapbox-gl-js)  
#### Databases support  
It should work with every **spatial** and **plain** (non-spatial) database, that works with django and geodjango.  
# Versions >1.4.0  
  Since version 1.4.0 the order of coordinates convention has been changed. Now the order is `longitude, latitude`. This change has been caused by support for spatial databases. Nevertheless, more user-friendly is order `latitude, longitude`(Google Maps uses it). That's why coordinates are falsely swapped in frontend and then after POST request in form field are swapped back into `longitude, latitude` order and saved to database.  
 My conclusion is that the location is falsely swapped in frontend and if you create location without our custom form field or just operate on a raw model in the backend, you will have to use the `longitude, latitude` order.  
 Versions before 1.4.0 always uses `latitude, longitude` order.  
# Installation  
Using pip:  
    `pip install django-mapbox-location-field`  
  
# Configuration  
* Add `"mapbox_location_field"` to `INSTALLED_APPS` in your settings file  
  
```python  
INSTALLED_APPS += ("mapbox_location_field",)  
```  
  
* Define [MAPBOX_KEY](https://docs.mapbox.com/help/how-mapbox-works/access-tokens/) in your settings file. This is vulnerable information which has to be passed to frontend, so it can be easily accessed by user. To ensure your safety, I would recommend using [url restrictions](https://docs.mapbox.com/help/how-mapbox-works/access-tokens/#url-restrictions) and [public scopes](https://docs.mapbox.com/help/how-mapbox-works/access-tokens/#scopes). More information on linked websites.  
```python  
MAPBOX_KEY = "pk.eyJ1IjoibWlnaHR5c2hhcmt5IiwiYSI6ImNqd2duaW4wMzBhcWI0M3F1MTRvbHB0dWcifQ.1sDAD43q0ktK1Sr374xGfw"  
```  
**PS. This above is only example access token. You have to paste here yours.**  
  
# Usage  
### PLAIN DATABASE  
 * Just create some model with LocationField.   
 ```python  
 from django.db import models from mapbox_location_field.models import LocationField  
 class SomeLocationModel(models.Model):  
	 location = LocationField()  
 ```
### SPATIAL DATABASE  
 * Just create some model with SpatialLocationField.  
```python  
 from django.db import models from mapbox_location_field.spatial.models import SpatialLocationField  
 class SomeLocationModel(models.Model):  
	 location = SpatialLocationField()    
 ```
* Create ModelForm  
 ```python  
 from django import forms from .models import Location  
 class LocationForm(forms.ModelForm):  
	 class Meta:  
		 model = Location 
		 fields = "__all__" 
 ```  
 Of course, you can also use CreateView, UpdateView or build Form yourself with `mapbox_location_field.forms.LocationField` or `mapbox_location_field.spatial.forms.SpatialLocationField` 
* Then just use it in html view. It can't be simpler!  
Paste this in your html head:  
```django  
 {% load mapbox_location_field_tags %} 
 {% location_field_includes %}
 {% include_jquery %}
 ```
 * And this in your body:  
 ```django  
 <form method="post">
 {% csrf_token %} 
	{{form}}
	<input type="submit" value="submit"> 
</form> 
{{ form.media }}
 ```
 * Your form is ready! Start your website and see how it looks. If you want to change something look to the [customization](#customization) section.  
 
# Customization  
In order to change few things you have to use `map_attrs` dictionary.  
Default `map_attrs` looks like this:  
```python  
default_map_attrs = {  
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
 "readonly": True,
 "placeholder": "Pick a location on map below", 
 "language": "auto",
 "message_404": "undefined address", }
 ```  
To change some values, just pass it when you create model.  
```python  
from django.db import models  
from mapbox_location_field.models import LocationField  
  
class Location(models.Model):  
    location = LocationField(map_attrs={"center": [0,0], "marker_color": "blue"})  
```  
## map_attrs  
* style - `<string>`, mapbox style url. Read more [here](https://docs.mapbox.com/help/glossary/style-url/).  
* zoom - `<int>`, map's zoom. Read more [here](https://docs.mapbox.com/help/glossary/zoom-level/).  
* center - `<list>` or `<tuple>` of `<float>`s, defaults map's center point in [`latitude`, `longitude`]  
* cursor_style - `<string>`, css cursor style. Read more [here](https://www.w3schools.com/cssref/pr_class_cursor.asp).  
* marker_color - `<string>` css color property. Read more [here](https://www.w3schools.com/cssref/css_colors_legal.asp)  and [here](https://www.w3schools.com/cssref/css_colors.asp).  
* rotate - `<bool>`, whether you can rotate the map with right mouse click or not.  
* geocoder -`<bool>`, whether geocoder searcher is showed or not.  
* fullscreen_button - `<bool>`, whether fullscreen button is showed or not.  
* navigation_buttons - `<bool>`, whether navigation buttons are showed or not.  
* track_location_button - `<bool>`, whether show my location button is showed or not.  
* readonly - `<bool>`, whether user can type location in text input  
* placeholder - `<string>`, text input's placeholder  
* id - `<string>`, unique id for the field, when you are using multiple fields (See more in [this section](#multiple-fields-usage)). When you use only one field, you don't have to define it, because default value is taken.  
* language - `<string>`, language of an address returned from geocoding queries. Default is `"auto"` - which lets mapbox gl js determine the language (usually browser language if available). Hovewer, you can specify it in case of need. Check out [language coverage section in mapbox docs](https://docs.mapbox.com/api/search/geocoding/#language-coverage) to see available options of this field.
* message_404 -  `<string>`, string used when no address is returned from geocoding query (e.q. marker on the ocean area). Default is simple: `"undefined address"`
  
## bootstrap  
MapInput widget is fully compatible with bootstrap library. I can even recommend using it with [django-bootstrap4](https://github.com/zostera/django-bootstrap4) or [django-crispy-forms](https://github.com/django-crispy-forms/django-crispy-forms).  
  
# Admin interface usage  
First create some model with location field like in [usage section](#usage).  
Then register it in admin interface like this:  
* #### Plain:  
```python  
from django.contrib import admin  
from .models import SomeLocationModel  
from mapbox_location_field.admin import MapAdmin  
  
admin.site.register(SomeLocationModel, MapAdmin)  
```  
* #### Spatial:  
```python  
from django.contrib import admin  
from .models import SomeLocationModel  
from mapbox_location_field.spatial.admin import SpatialMapAdmin  
  
admin.site.register(SomeLocationModel, SpatialMapAdmin)  
```  
* #### Admin customization:  
Since `v1.7.0` admin customization should work out of the box, automatically using the `map_attrs` from model definition. 
  
# AddressAutoHiddenField  
AddressAutoHiddenField is a field for storing address. It uses AddressAutoHiddenInput which is hidden and when you place your marker on the map, automatically fill itself with proper address.  
In order to use it just add it to your model. Something like this:  
```python  
class Location(models.Model):  
    location = LocationField()  
    address = AddressAutoHiddenField()  
```  
# Multiple fields usage  
Since version 1.6.0, it is now possible to use multiple LocationFields (or forms or widgets) as well as multiple AutoHiddenAddressFields. All you have to do is define unique `id` in `map_attrs`:  
```python  
location1 = LocationField(map_attrs={"id": "unique_id_1"})  
location2 = LocationField(map_attrs={"id": "unique_id_2"})  
```  
Then you can also use these ids as `map_id` in your AutoHiddenAddressFields:  
```python  
address1 = AddressAutoHiddenField(map_id="unique_id_1")  
address2 = AddressAutoHiddenField(map_id="unique_id_2")  
```  
# Troubleshooting  
* #### Usage of the plain field's value in javascript ( [Issue #21](https://github.com/Simon-the-Shark/django-mapbox-location-field/issues/21))
	In case of the plain field, the python representation of coordinates is a  [tuple](https://www.w3schools.com/python/python_tuples.asp). And e.g. Mapbox requires a [javascript's array](https://www.w3schools.com/js/js_arrays.asp) when placing a marker on a map, which has identical syntax as  [Python's list](https://www.w3schools.com/python/python_lists.asp). In order to make the transformation as easy as possible, since `v1.6.4` you can use a special filter or tag (
choose your preferred way)
	```Django
	{% load mapbox_location_field_tags %}
	<script>
		var lngLatWithFilter = {{object.location | tuple_to_array }};
		var lngLatWithTag = {% tuple_to_array object.location %};
	
	// These are just two ways, which give the same result
	// Now you can use one of this variables as an array
	</script>
	```
 * Stackoverflow questions:
    * [Unable to show the data in django-mapbox-location-field Django
](https://stackoverflow.com/questions/66081209/unable-to-show-the-data-in-django-mapbox-location-field-django/66094192#66094192)
# Technologies  
* Django  
* mapbox gl js  
* jQuery  
* html and css
