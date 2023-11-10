window.onload = function () {
  fetch("/api/systems")
    .then((response) => response.json())
    .then((data) => {
      const systemsContainer = document.getElementById("systems-container");
      data.forEach((system) => {
        const button = document.createElement("button");
        button.innerText = system.SystemName;
        button.addEventListener("click", () =>
          loadChargesForSystem(system.SystemID)
        );
        systemsContainer.appendChild(button);
      });
    })
    .catch((error) => console.error("Error fetching systems:", error));
};

function loadChargesForSystem(systemId) {
  const chargesTable = document.getElementById("charges-table");
  chargesTable.innerHTML = ""; // Clear previous table data

  fetch(`/api/charges/system/${systemId}`)
    .then((response) => response.json())
    .then((response) => {
      const { data: chargeData, columns: columnOrder } = response;
      if (chargeData && chargeData.length > 0) {
        // Create table headers
        const thead = document.createElement("thead");
        const headerRow = thead.insertRow();
        columnOrder.forEach((header) => {
          const th = document.createElement("th");
          th.textContent = header;
          headerRow.appendChild(th);
        });
        chargesTable.appendChild(thead);

        // Create table body
        const tbody = document.createElement("tbody");
        chargeData.forEach((item) => {
          const row = tbody.insertRow();
          columnOrder.forEach((header) => {
            const cell = row.insertCell();
            cell.textContent = item[header];
          });
        });
        chargesTable.appendChild(tbody);
      } else {
        // Handle no data
        console.log("No charge data available for this system.");
      }
    })
    .catch((error) => console.error("Error fetching charge data:", error));
}
