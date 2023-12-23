var oTable;
const colorMapping = {
  1: "#a5a7d4",
  2: "#a30046",
  3: "#2361fd",
  4: "#63599e",
  5: "#006937",
  6: "#800000",
};

document.addEventListener("DOMContentLoaded", (event) => {
  // Code that needs the DOM to be ready can go here
  var addToChargesheetButton = document.getElementById("addToChargesheet");
  if (addToChargesheetButton) {
    addToChargesheetButton.addEventListener("click", function () {
      var selectedData = oTable.rows({ selected: true }).data().toArray();
      addToChargesheet(selectedData);
    });
  }

  initPage();
});

async function initPage() {
  try {
    // Fetch and display systems
    const systems = await fetchSystems();
    displaySystems(systems);

    // Fetch and display locations for the first system by default
    if (systems.length > 0) {
      const systemId = systems[0].SystemID;
      const locations = await fetchLocations(systemId);
      displayLocations(locations);
    }
  } catch (error) {
    console.error("Error initializing page:", error);
  }
}

async function fetchSystems() {
  const response = await fetch("/api/systems");
  if (!response.ok) {
    throw new Error("Error fetching systems.");
  }
  return response.json();
}

function displaySystems(systems) {
  const systemsContainer = document.getElementById("systems-container");

  systems.forEach((system) => {
    const button = createButton(system.SystemName, "system-button");
    const backgroundColor = colorMapping[system.SystemID];
    button.style.backgroundColor = backgroundColor;
    button.style.color = "white"; // Set text color to white
    button.addEventListener("click", async () => {
      document
        .querySelectorAll(".system-button")
        .forEach((btn) => btn.classList.remove("selected"));
      button.classList.add("selected");
      const locations = await fetchLocations(system.SystemID);
      displayLocations(locations);
    });
    systemsContainer.appendChild(button);
  });
}

async function fetchLocations(systemId) {
  const response = await fetch(`/api/locations/${systemId}`);
  if (!response.ok) {
    throw new Error("Error fetching locations.");
  }
  return response.json();
}

function displayLocations(locations) {
  const locationsContainer = document.getElementById("locations-container");
  locationsContainer.innerHTML = ""; // Clear existing buttons

  locations.forEach((location) => {
    const locButton = createButton(location.LocationName, "location-button");
    const backgroundColor = colorMapping[location.SystemID]; // Use colorMapping
    locButton.style.backgroundColor = backgroundColor;
    locButton.style.color = "white"; // Set text color to white
    locButton.addEventListener("click", async () => {
      const locationDetails = await fetchLocationDetails(location.LocationID);
      displayLocationDetails(locationDetails);

      // Remove existing system color class (if any)
      document
        .getElementById("location-information")
        .classList.remove("system-color");

      // Add the new system color class based on location.SystemID
      document
        .getElementById("location-information")
        .classList.add(`system-color-${location.SystemID}`);

      loadChargesForLocation(location.SystemID, location.LocationID); // Pass SystemID and LocationID
    });
    locationsContainer.appendChild(locButton);
  });
}

async function fetchLocationDetails(locationId) {
  const response = await fetch(`/api/locations/details/${locationId}`);
  if (!response.ok) {
    throw new Error("Error fetching location details.");
  }
  return response.json();
}

function displayLocationDetails(locationDetails) {
  const infoContainer = document.getElementById("location-information");
  infoContainer.innerHTML = `
    <p>Name: ${locationDetails.LocationName}</p>
    <p>Address: ${locationDetails.Address}, ${locationDetails.City}, ${locationDetails.State} ${locationDetails.ZipCode}</p>
    <p>Phone: ${locationDetails.Phone}</p>
  `;
}
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
  const filteredColumns = columns.filter(
    (column) => column !== "LocationID" && column !== "SystemID"
  );
  filteredColumns.forEach((column) => {
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
    filteredColumns.forEach((column) => {
      const td = document.createElement("td");
      td.textContent = row[column];
      tr.appendChild(td);
    });
    tbody.appendChild(tr);
  });
  table.appendChild(tbody);

  // Initialize the DataTable with filtered columns
  oTable = $(table).DataTable({
    columns: filteredColumns.map((column) => ({ title: column, data: column })),
    dom: "Bfrtip", // Define the elements and their order in the DOM
    buttons: [
      "copy", // Enable the copy to clipboard button
      "csv", // Enable the CSV export button
      "excel", // Enable the Excel export button
      "pdf", // Enable the PDF export button
      "print", // Enable the print view button
      "colvis", // Enable column visibility toggle button
    ],
    select: true, // Enable select extension
    paging: true, // Enable pagination
    searching: true, // Enable searching
    ordering: true, // Enable column ordering
    info: true, // Enable the information summary
    responsive: true, // Enable responsive design for mobile devices
    colReorder: true, // Enable column reordering
    // Additional options here...
    initComplete: function (settings, json) {},
  });

  // Additional code as needed
}

function clearChargesheet() {
  if (confirm("Are you sure you want to clear the chargesheet?")) {
    var chargesheetList = document.getElementById("chargesheetList");
    chargesheetList.innerHTML = "";
  }
}

function isValidValue(value) {
  return value !== null && value !== undefined && value !== "";
}

function shouldExcludeKey(key) {
  // Add any keys here that you don't want to include in the chargesheet
  const excludedKeys = ["SystemID", "LocationID", "CodeID", "Type"];
  return excludedKeys.includes(key);
}

// Updated createInfoDiv function
function createInfoDiv(key, value) {
  var infoDiv = document.createElement("div");
  infoDiv.className = "charge-info";

  var keySpan = document.createElement("span");
  keySpan.className = "charge-key";
  keySpan.textContent = key + ": ";

  var valueSpan = document.createElement("span");
  valueSpan.className = "charge-value";
  valueSpan.textContent = value;

  infoDiv.appendChild(keySpan);
  infoDiv.appendChild(valueSpan);
  return infoDiv;
}

function createRemoveButton(listItem) {
  var removeBtn = document.createElement("button");
  removeBtn.className = "remove-charge";
  removeBtn.textContent = "Remove";
  removeBtn.onclick = function () {
    listItem.remove();
  };
  return removeBtn;
}

function addToChargesheet(selectedData) {
  if (selectedData.length === 0) {
    console.error("No data selected.");
    return;
  }

  var chargesheetList = document.getElementById("chargesheetList");

  selectedData.forEach(function (data) {
    var listItem = document.createElement("li");
    listItem.className = "chargesheet-item";

    for (var key in data) {
      if (
        data.hasOwnProperty(key) &&
        isValidValue(data[key]) &&
        !shouldExcludeKey(key)
      ) {
        console.log("Key:", key); // Debugging statement
        console.log("Value:", data[key]); // Debugging statement

        var infoDiv = createInfoDiv(key, data[key]);
        listItem.appendChild(infoDiv);
      }
    }

    var removeBtn = createRemoveButton(listItem);
    listItem.appendChild(removeBtn);
    chargesheetList.appendChild(listItem);
  });

  // Deselect rows in oTable (assuming oTable is defined elsewhere)
  oTable.rows({ selected: true }).deselect();
}

function createButton(text, className) {
  var button = document.createElement("button");
  button.textContent = text;
  button.className = className; // Existing class
  // Add Bootstrap classes
  button.classList.add("btn", "btn-lg");
  return button;
}
