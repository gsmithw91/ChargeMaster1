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
          loadChargesForSystem(system.SystemID);
        });
        systemsContainer.appendChild(button);
      });
    })
    .catch((error) => console.error("Error fetching systems:", error));
};
let isDataTableInitialized = false;
function loadChargesForSystem(systemId) {
  // Get the charges table element
  const chargesTable = $("#charges-table");

  // Check if the DataTable instance already exists and destroy it if so
  if ($.fn.DataTable.isDataTable("#charges-table")) {
    chargesTable.DataTable().clear().destroy();
  }

  // Clear the table element itself
  chargesTable.empty();

  fetch(`/api/charges/system/${systemId}`)
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
        console.log("No charge data available for this system.");
      }
    })
    .catch((error) => console.error("Error fetching charge data:", error));
}
