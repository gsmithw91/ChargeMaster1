$(document).ready(function() {
  loadSystems();
});

function loadSystems() {
  $.getJSON('/api/systems', function(systems) {
    systems.forEach(function(system) {
      var button = $('<button>')
        .addClass('btn system-btn')
        .text(system.SystemName)
        .data('system-id', system.SystemID)
        .click(function() {
          // When a system button is clicked, load locations for that system
          loadLocations($(this).data('system-id'));
        });
      $('#systems-container').append(button);
    });
  });
}

function loadLocations(systemId) {
  $.getJSON(`/api/locations/${systemId}`, function(locations) {
    $('#locations-container').empty(); // Clear any existing buttons
    locations.forEach(function(location) {
      var button = $('<button>')
        .addClass('btn location-btn')
        .text(location.LocationName)
        .data('location-id', location.LocationID)
        .click(function() {
          // Handle location button click event
        });
      $('#locations-container').append(button);
    });
  });
}
