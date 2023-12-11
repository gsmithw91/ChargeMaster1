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
