window.onload = function () {
  fetch("/api/systems")
    .then((response) => response.json())
    .then((data) => {
      const systemsContainer = document.getElementById("systems-container");
      data.forEach((system) => {
        const button = document.createElement("button");
        button.innerText = system.SystemName;
        button.addEventListener("click", function () {
          // Call the function to load charges for the selected system
          loadChargesForSystem(system.SystemID);
        });
        systemsContainer.appendChild(button);
      });
    })
    .catch((error) => {
      console.error("Error fetching systems:", error);
    });
};
function loadChargesForSystem(systemId) {
  const chargesContainer = document.getElementById("charges-container");
  const chargesTable = document.getElementById("charges-table");
  chargesTable.innerHTML = ""; // Clear the table

  fetch(`/api/charges/system/${systemId}`)
    .then((response) => response.json())
    .then((response) => {
      const { data: chargeData, columns: columnOrder } = response;
      if (chargeData && chargeData.length > 0 && columnOrder) {
        // Create thead and tbody elements
        const thead = chargesTable.createTHead();
        const tbody = document.createElement("tbody");
        chargesTable.appendChild(tbody);

        // Create table headers using the column order from the response
        const headerRow = thead.insertRow();
        columnOrder.forEach((header) => {
          const th = document.createElement("th");
          th.textContent = header; // Assuming column names are already formatted
          headerRow.appendChild(th);
        });

        // Create table rows using the column order from the response
        chargeData.forEach((item) => {
          const row = tbody.insertRow();
          columnOrder.forEach((header) => {
            const cell = row.insertCell();
            cell.textContent = item[header];
          });
        });
      } else {
        // If no data or no column order, clear the table and display a message
        chargesTable.innerHTML = "";
        const noDataMessage = document.createElement("p");
        noDataMessage.textContent = "No charge data available for this system.";
        chargesContainer.appendChild(noDataMessage);
      }
    })
    .catch((error) => {
      console.error("Error fetching charge data:", error);
    });
}
