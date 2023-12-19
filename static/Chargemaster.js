// Define global variable for DataTable
var oTable;

// Execute once the DOM is fully loaded
document.addEventListener("DOMContentLoaded", (event) => {
  // Initialize the page setup
  initPage();
});

// Function to initialize the page
function initPage() {
  // Fetch the list of hospital systems from the API and display them
  fetchSystems();
}

// Fetches hospital systems from the API and adds them to the page
function fetchSystems() {
  fetch("/api/systems")
    .then((response) => response.json())
    .then((data) => {
      // Target the container for displaying system buttons
      const systemsContainer = document.getElementById("systems-container");
      // Iterate over each system and create a button for it
      data.forEach((system) => {
        const button = document.createElement("button");
        button.className = "system-button";
        button.innerText = system.SystemName;
        // Add event listener for each system button
        button.addEventListener("click", function () {
          // Highlight the selected system and fetch its locations
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

// Fetches and displays locations for a given system
function fetchAndDisplayLocations(systemId) {
  fetch(`/api/locations/${systemId}`)
    .then((response) => response.json())
    .then((locations) => {
      // Target the container for displaying location buttons
      const locationsContainer = document.getElementById("locations-container");
      locationsContainer.innerHTML = ""; // Clear existing location buttons

      // Iterate over each location and create a button
      locations.forEach((location) => {
        const locButton = document.createElement("button");
        locButton.className = "location-button";
        locButton.innerText = location.LocationName;

        // Add event listener to each location button
        locButton.addEventListener("click", () => {
          // Fetch and display details for the selected location
          // and load its charge data
          fetchAndDisplayLocationDetails(location.LocationID);
          loadChargesForLocation(systemId, location.LocationID);
        });

        locationsContainer.appendChild(locButton);
      });
    })
    .catch((error) => console.error("Error fetching locations:", error));
}

// Fetches and displays details for a specific location
function fetchAndDisplayLocationDetails(locationId) {
  fetch(`/api/locations/details/${locationId}`)
    .then((response) => response.json())
    .then((locationDetails) => {
      // Target the container for displaying location information
      const infoContainer = document.getElementById("location-information");
      // Populate the container with location details
      infoContainer.innerHTML = `
        <h2>Location Information</h2>
        <p>Name: ${locationDetails.LocationName}</p>
        <p>Address: ${locationDetails.Address}, ${locationDetails.City}, ${locationDetails.State} ${locationDetails.ZipCode}</p>
        <p>Phone: ${locationDetails.Phone}</p>
      `;
    })
    .catch((error) => console.error("Error fetching location details:", error));
}

// Fetches and displays the charges data for a specific location
function loadChargesForLocation(systemId, locationId) {
  // Construct the API endpoint URL
  let apiUrl = `/api/charges/system/${systemId}/location/${locationId}`;
  fetch(apiUrl)
    .then((response) => {
      if (!response.ok) {
        throw new Error("No charge data available for this location.");
      }
      return response.json();
    })
    .then((data) => {
      // Display the charge data in a DataTable
      displayChargesData(data.data, data.columns);
    })
    .catch((error) => {
      console.error(error.message);
      // Handle the error (e.g., display a message to the user)
    });
}

// Displays charge data in a DataTable
function displayChargesData(chargeData, columns) {
  // Target the container for the charges table and reset its content
  const chargesContainer = document.getElementById("charges-container");
  chargesContainer.innerHTML = "";
  const table = document.createElement("table");
  table.id = "charges-table";
  table.className = "display";
  chargesContainer.appendChild(table);

  // Construct the header row for the table
  const thead = document.createElement("thead");
  const headerRow = document.createElement("tr");
  columns.forEach((column) => {
    const th = document.createElement("th");
    th.textContent = column;
    headerRow.appendChild(th);
  });
  thead.appendChild(headerRow);
  table.appendChild(thead);

  // Construct the body of the table with charge data
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

  // Initialize the DataTable with custom options
  oTable = $(table).DataTable({
    // DataTables configuration options
    columns: columns.map((column) => ({ title: column, data: column })),
    dom: "Bfrtip",
    buttons: [
      // Define buttons for DataTables functionality
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
