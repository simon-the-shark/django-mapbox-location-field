$(function() {
  $(document).on("reverse-geocode", function (e, map_id, input) {
    x = $("#" + map_id + ".js-mapbox-address-input-location-field");
    x.val(input);
  });
});
