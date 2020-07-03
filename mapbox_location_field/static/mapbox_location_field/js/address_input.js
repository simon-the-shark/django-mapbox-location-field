$(document).on("reverse-geocode", function (e, map_id, input) {
    $("#" + map_id + ".js-mapbox-address-input-location-field").val(input);
});