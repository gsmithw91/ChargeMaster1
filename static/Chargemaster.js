var oTable;

// Attach event handlers or run initial setup code inside this listener
document.addEventListener("DOMContentLoaded", (event) => {
  // Code that needs the DOM to be ready can go here
  // For instance, initializing event listeners or fetching initial data
  initPage();
  document
    .getElementById("addToChargesheet")
    .addEventListener("click", function () {
      var selectedData = oTable.rows({ selected: true }).data();
      addToChargesheet(selectedData);
    });
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

// Event listener for the "Add to Chargesheet" button
document.addEventListener("DOMContentLoaded", (event) => {
  // Code that needs the DOM to be ready can go here
  initPage(); // Make sure this function is defined elsewhere in your code
});

// Function to add selected items to the Chargesheet
function addToChargesheet() {
  var selectedData = oTable.rows({ selected: true }).data().toArray();

  if (selectedData.length === 0) {
    console.error("No data selected.");
    return;
  }

  var chargesheetList = document.getElementById("chargesheetList");

  selectedData.forEach(function (data) {
    // Create a container for the charge item
    var listItem = document.createElement("li");
    listItem.className = "chargesheet-item";

    // Iterate over each property in the data object
    for (var key in data) {
      if (data.hasOwnProperty(key)) {
        var value = data[key];

        // Create a div to hold the key-value pair
        var infoDiv = document.createElement("div");
        infoDiv.className = "charge-info";

        // Create a span for the key
        var keySpan = document.createElement("span");
        keySpan.className = "charge-key";
        keySpan.textContent = key + ": ";

        // Create a span for the value
        var valueSpan = document.createElement("span");
        valueSpan.className = "charge-value";
        valueSpan.textContent = value;

        // Append the key and value spans to the infoDiv
        infoDiv.appendChild(keySpan);
        infoDiv.appendChild(valueSpan);

        // Append the infoDiv to the listItem
        listItem.appendChild(infoDiv);
      }
    }

    // Optionally, add a remove button to each listItem
    var removeBtn = document.createElement("button");
    removeBtn.className = "remove-charge";
    removeBtn.textContent = "Remove";
    removeBtn.onclick = function () {
      listItem.remove();
    };
    listItem.appendChild(removeBtn);

    // Append the listItem to the chargesheetList
    chargesheetList.appendChild(listItem);
  });

  oTable.rows({ selected: true }).deselect(); // Deselect after adding
}
