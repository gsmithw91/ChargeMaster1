document.addEventListener("DOMContentLoaded", (event) => {
  var addToChargesheetButton = document.getElementById("addToChargesheet");
  if (addToChargesheetButton) {
    addToChargesheetButton.addEventListener("click", function () {
      var selectedData = oTable.rows({ selected: true }).data().toArray();
      addToChargesheet(selectedData);
    });
  }
  const exportPdfButton = document.getElementById("exportPdfButton");
  if (exportPdfButton) {
    exportPdfButton.addEventListener("click", () => exportChargesheetAsPDF());
  }

  // Updated to match the ID in your HTML
  const clearChargesButton = document.getElementById("clearChargesButton");
  if (clearChargesButton) {
    clearChargesButton.addEventListener("click", clearChargesheet);
  }
});

function clearChargesheet() {
  if (confirm("Are you sure you want to clear the chargesheet?")) {
    var chargesheetList = document.getElementById("chargesheetList");
    chargesheetList.innerHTML = "";
  }
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
        var infoDiv = createInfoDiv(key, data[key]);
        listItem.appendChild(infoDiv);
      }
    }

    var removeBtn = createRemoveButton(listItem);
    listItem.appendChild(removeBtn);
    chargesheetList.appendChild(listItem);
  });

  oTable.rows({ selected: true }).deselect();
}

function isValidValue(value) {
  return value !== null && value !== undefined && value !== "";
}

function shouldExcludeKey(key) {
  // Add any keys here that you don't want to include in the chargesheet
  const excludedKeys = ["SystemID", "LocationID", "CodeID", "Type"];
  return excludedKeys.includes(key);
}

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
function exportChargesheetAsPDF() {
  const chargesheetElement = document.getElementById("chargesheetContainer");

  // Check if the chargesheetElement exists
  if (!chargesheetElement) {
    console.error("Chargesheet container element not found.");
    return;
  }

  const buttonRow = document.querySelector(".button-row");

  // Check if the buttonRow exists
  if (!buttonRow) {
    console.error("Button row element not found.");
    return;
  }

  // Temporarily hide the button row
  buttonRow.classList.add("hidden");

  html2canvas(chargesheetElement)
    .then((canvas) => {
      const imgData = canvas.toDataURL("image/png");
      const pdf = new jsPDF({
        orientation: "portrait",
        unit: "px",
        format: [canvas.width, canvas.height],
      });

      pdf.addImage(imgData, "PNG", 0, 0, canvas.width, canvas.height);
      pdf.save("chargesheet.pdf");

      // Show the button row again
      buttonRow.classList.remove("hidden");
    })
    .catch((err) => {
      console.error("Error exporting PDF:", err);
      // Show the button row again in case of error
      buttonRow.classList.remove("hidden");
    });
}

function sendChargeSheetData() {
  var selectedData = oTable.rows({ selected: true }).data().toArray();

  fetch("/process-chargesheet", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(selectedData),
  })
    .then((response) => response.json())
    .then((data) => console.log("Processed data:", data))
    .catch((error) => console.error("Error:", error));
}
