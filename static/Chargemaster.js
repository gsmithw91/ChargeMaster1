var oTable;

document.addEventListener("DOMContentLoaded", (event) => {
  // Code that needs the DOM to be ready can go here
  initPage();
});

function initPage() {
  // You might fetch the initial system list here, for example
  fetchSystems();
}

function fetchSystems() {
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

        // When a location button is clicked, fetch and display location details
        // and fetch and display charges for this location
        locButton.addEventListener("click", () => {
          fetchAndDisplayLocationDetails(location.LocationID); // Fetch location details
          loadChargesForLocation(systemId, location.LocationID); // Fetch charges for this location
        });

        locationsContainer.appendChild(locButton);
      });
    })
    .catch((error) => console.error("Error fetching locations:", error));
}

// This function fetches and displays details for a specific location
function fetchAndDisplayLocationDetails(locationId) {
  fetch(`/api/locations/details/${locationId}`)
    .then((response) => response.json())
    .then((locationDetails) => {
      const infoContainer = document.getElementById("location-information");
      infoContainer.innerHTML = `
        <h2>Location Information</h2>
        <p>Name: ${locationDetails.LocationName}</p>
        <p>Address: ${locationDetails.Address}, ${locationDetails.City}, ${locationDetails.State} ${locationDetails.ZipCode}</p>
        <p>Phone: ${locationDetails.Phone}</p>
      `;
    })
    .catch((error) => console.error("Error fetching location details:", error));
}

// This function fetches and displays the charges data for a specific location in a DataTable
function loadChargesForLocation(systemId, locationId) {
  let apiUrl = `/api/charges/system/${systemId}/location/${locationId}`;
  fetch(apiUrl)
    .then((response) => {
      if (!response.ok) {
        throw new Error("No charge data available for this location.");
      }
      return response.json();
    })
    .then((data) => {
      displayChargesData(data.data, data.columns);
    })
    .catch((error) => {
      console.error(error.message);
      // Handle the error by showing a message to the user or logging
    });
}

function displayChargesData(chargeData, columns) {
  // Clear previous table contents and create a new table element
  const chargesContainer = document.getElementById("charges-container");
  chargesContainer.innerHTML = "";
  const table = document.createElement("table");
  table.id = "charges-table";
  table.className = "display";
  chargesContainer.appendChild(table);

  // Create the header row
  const thead = document.createElement("thead");
  const headerRow = document.createElement("tr");
  columns.forEach((column) => {
    const th = document.createElement("th");
    th.textContent = column;
    headerRow.appendChild(th);
  });
  thead.appendChild(headerRow);
  table.appendChild(thead);

  // Create the body of the table
  const tbody = document.createElement("tbody");
  chargeData.forEach((row) => {
    const tr = document.createElement("tr");
    columns.forEach((column) => {
      const td = document.createElement("td");
      td.textContent = row[column];
      tr.appendChild(td);
    });
    tbody.appendChild(tr);
  });
  table.appendChild(tbody);

  // Initialize the DataTable with the options
  oTable = $(table).DataTable({
    columns: columns.map((column) => ({ title: column, data: column })),
    dom: "Bfrtip",
    buttons: [
      {
        extend: "colvis",
        text: "Select columns",
        className: "btn-colvis",
      },
      "copy",
      "csv",
      "excel",
      "pdf",
      "print",
    ],
    select: "multi", // Enable multi-row selection
    paging: true,
    searching: true,
    ordering: true,
    info: true,
  });
}
