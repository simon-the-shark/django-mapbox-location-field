function translate_to_string(obj) {
    var lat = obj.lat;
    var lng = obj.lng;
    return lat + "," + lng
}

var input = $(".js-mapbox-input-location-field");
var map = new mapboxgl.Map({
    container: 'secret-id-map-mapbox-location-field',
    style: 'mapbox://styles/mapbox/outdoors-v11',
    center: [17.031645, 51.106715],
    zoom: 13
});
var geocoder = new MapboxGeocoder({
    accessToken: mapboxgl.accessToken,
    mapboxgl: mapboxgl,
});

map.getCanvas().style.cursor = 'pointer';
map.dragRotate.disable();
map.touchZoomRotate.disableRotation();

map.addControl(new mapboxgl.GeolocateControl({
    positionOptions: {
        enableHighAccuracy: true
    },
    trackUserLocation: true
}));
map.addControl(geocoder, "top-left");
map.addControl(new mapboxgl.FullscreenControl());
map.addControl(new mapboxgl.NavigationControl());

geocoder.on("result", function (e) {
    $("div.mapboxgl-marker.mapboxgl-marker-anchor-center").not(".mapboxgl-user-location-dot").remove();
    input.val(e.result.geometry.coordinates);
    var marker = new mapboxgl.Marker({draggable: true,});
    marker.setLngLat(e.result.geometry.coordinates)
        .addTo(map);
});

map.on("click", function (e) {
    $("div.mapboxgl-marker.mapboxgl-marker-anchor-center").not(".mapboxgl-user-location-dot").remove();
    input.val(translate_to_string(e.lngLat));
    var marker = new mapboxgl.Marker({draggable: true,});
    marker.setLngLat(e.lngLat)
        .addTo(map);
});
