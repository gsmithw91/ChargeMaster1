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
          fetchAndDisplayLocationDetails(location.LocationID); // Correctly called here
        });
        locationsContainer.appendChild(locButton);
      });
    })
    .catch((error) => console.error("Error fetching locations:", error));
}

function fetchAndDisplayLocationDetails(locationId) {
  fetch(`/api/locations/details/${locationId}`)
    .then((response) => response.json())
    .then((locationDetails) => {
      const infoContainer = document.getElementById("location-information");
      // Assume locationDetails is the object with the location information
      infoContainer.innerHTML = `
        <h2>Location Information</h2>
        <p>Name: ${locationDetails.LocationName}</p>
        <p>Address: ${locationDetails.Address}, ${locationDetails.City}, ${locationDetails.State} ${locationDetails.ZipCode}</p>
        <p>Phone: ${locationDetails.Phone}</p>
      `;
    })
    .catch((error) => console.error("Error fetching location details:", error));
}

function loadChargesForLocation(systemId, locationId) {
  let apiUrl = "/api/charges";
  if (systemId) {
    apiUrl += `/system/${systemId}`;
    if (locationId) {
      apiUrl += `/location/${locationId}`;
    }
  }

  fetch(apiUrl)
    .then((response) => response.json())
    .then((data) => {
      if (data.error) {
        console.error("Error fetching charge data:", data.error);
        // Handle error - e.g., display a message to the user
      } else {
        displayChargesData(data.data, data.columns);
      }
    })
    .catch((error) => {
      console.error("Error fetching charge data:", error);
      // Handle fetch error - e.g., display a message to the user
    });
}

function displayChargesData(chargeData, columns) {
  const chargesContainer = document.getElementById("charges-container");
  chargesContainer.innerHTML = ""; // Clear previous table

  // Create a table element
  const table = document.createElement("table");
  table.id = "charges-table";
  table.className = "display";

  // Create the headers
  const thead = document.createElement("thead");
  const headerRow = document.createElement("tr");
  columns.forEach((column) => {
    const th = document.createElement("th");
    th.textContent = column;
    headerRow.appendChild(th);
  });
  thead.appendChild(headerRow);
  table.appendChild(thead);

  // Create the table body
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

  chargesContainer.appendChild(table);

  // Initialize DataTable
  $(table).DataTable({
    // DataTables configuration options
    paging: true,
    pageLength: 25,
    searching: true,
    ordering: true,
    order: [[1, "asc"]], // Assuming you want to order by the second column initially
    scrollY: "50vh",
    scrollCollapse: true,
    language: {
      search: "Filter records:",
      paginate: {
        first: "First",
        last: "Last",
        next: "Next",
        previous: "Previous",
      },
      info: "Showing _START_ to _END_ of _TOTAL_ entries",
    },
    dom: "Bfrtip",
    buttons: ["copy", "csv", "excel", "pdf", "print"],
    responsive: true,
    stateSave: false,
  });
}
