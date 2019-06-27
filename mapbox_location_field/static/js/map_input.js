var coordinatesGeocoder = function (query) {
// match anything which looks like a decimal degrees coordinate pair
    var matches = query.match(/^[ ]*(?:Lat: )?(-?\d+\.?\d*)[, ]+(?:Lng: )?(-?\d+\.?\d*)[ ]*$/i);
    if (!matches) {
        return null;
    }

    function coordinateFeature(lng, lat) {
        return {
            center: [lng, lat],
            geometry: {
                type: "Point",
                coordinates: [lng, lat]
            },
            place_name: 'Lat: ' + lat + ' Lng: ' + lng, // eslint-disable-line camelcase
            place_type: ['coordinate'], // eslint-disable-line camelcase
            properties: {},
            type: 'Feature'
        };
    }

    var coord1 = Number(matches[1]);
    var coord2 = Number(matches[2]);
    var geocodes = [];

    if (coord1 < -90 || coord1 > 90) {
// must be lng, lat
        geocodes.push(coordinateFeature(coord1, coord2));
    }

    if (coord2 < -90 || coord2 > 90) {
// must be lat, lng
        geocodes.push(coordinateFeature(coord2, coord1));
    }

    if (geocodes.length === 0) {
// else could be either lng, lat or lat, lng
        geocodes.push(coordinateFeature(coord1, coord2));
        geocodes.push(coordinateFeature(coord2, coord1));
    }

    return geocodes;
};

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
    localGeocoder: coordinatesGeocoder,

});

map.getCanvas().style.cursor = 'pointer';
map.dragRotate.disable();
map.touchZoomRotate.disableRotation();

map.addControl(new mapboxgl.GeolocateControl({
    positionOptions: {
        enableHighAccuracy: true
    },
    trackUserLocation: true,
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
