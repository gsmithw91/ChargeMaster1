window.onload = function () {
  fetch("/api/systems")
    .then((response) => response.json())
    .then((data) => {
      const systemsContainer = document.getElementById("systems-container");
      data.forEach((system) => {
        const button = document.createElement("button");
        button.className = "system-button";
        button.innerText = system.SystemName;
        button.addEventListener("click", function () {
          document
            .querySelectorAll(".system-button")
            .forEach((btn) => btn.classList.remove("selected"));
          button.classList.add("selected");
          fetchAndDisplayLocations(system.SystemID);
        });
        systemsContainer.appendChild(button);
      });
    })
    .catch((error) => console.error("Error fetching systems:", error));
};

let map;

function initMap(latitude, longitude) {
  const location = { lat: latitude, lng: longitude };
  map = new google.maps.Map(document.getElementById("map-container"), {
    center: location,
    zoom: 14,
  });

  new google.maps.Marker({
    position: location,
    map: map,
  });
}

function fetchAndDisplayLocations(systemId) {
  fetch(`/api/locations/${systemId}`)
    .then((response) => response.json())
    .then((locations) => {
      const locationsContainer = document.getElementById("locations-container");
      locationsContainer.innerHTML = ""; // Clear existing buttons
      locations.forEach((location) => {
        const locButton = document.createElement("button");
        locButton.className = "location-button";
        locButton.innerText = location.LocationName;
        locButton.addEventListener("click", () => {
          loadChargesForLocation(systemId, location.LocationID);
          displayLocationInformation(location.LocationID); // Call to display location information
        });
        locationsContainer.appendChild(locButton);
      });
    })
    .catch((error) => console.error("Error fetching locations:", error));
}

function loadChargesForLocation(systemId, locationId) {
  const chargesTable = $("#charges-table");
  if ($.fn.DataTable.isDataTable("#charges-table")) {
    chargesTable.DataTable().clear().destroy();
  }
  chargesTable.empty();
  fetch(`/api/charges/location/${systemId}/${locationId}`)
    .then((response) => response.json())
    .then((response) => {
      if (response.data && response.data.length > 0) {
        chargesTable.DataTable({
          data: response.data,
          columns: response.columns.map((col) => ({ title: col, data: col })),
          paging: true,
          searching: true,
          ordering: true,
          scrollX: true,
          fixedHeader: true,
        });
      } else {
        console.log("No charge data available for this location.");
      }
    })
    .catch((error) => console.error("Error fetching charge data:", error));
}

function displayLocationInformation(locationId) {
  fetch(`/api/locations/details/${locationId}`)
    .then((response) => response.json())
    .then((data) => {
      const infoContainer = document.getElementById("location-information");
      infoContainer.innerHTML = ""; // Clear existing information
      // Create and append the HTML content for the location information
      const detailsHTML = `
        <h2>Location Information</h2>
        <p>Name: ${data.LocationName}</p>
        <p>Address: ${data.Address}, ${data.City}, ${data.State} ${data.ZipCode}</p>
        <p>Phone: ${data.Phone}</p>
      `;
      infoContainer.innerHTML = detailsHTML;
    })
    .catch((error) =>
      console.error("Error fetching location information:", error)
    );
}
