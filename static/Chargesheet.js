// Listen for the DOMContentLoaded event to ensure the DOM is fully loaded before executing the script
document.addEventListener("DOMContentLoaded", (event) => {
  // Attach event listener to the "Add to Chargesheet" button
  var addToChargesheetButton = document.getElementById("addToChargesheet");
  if (addToChargesheetButton) {
    addToChargesheetButton.addEventListener("click", function () {
      // Retrieve selected rows from the DataTable
      var selectedData = oTable.rows({ selected: true }).data().toArray();
      // Add the selected rows to the chargesheet
      addToChargesheet(selectedData);
    });
  }

  // Attach event listener to the "Export as PDF" button
  const exportPdfButton = document.getElementById("exportPdfButton");
  if (exportPdfButton) {
    exportPdfButton.addEventListener("click", () => exportChargesheetAsPDF());
  }
});

// Function to add selected data to the chargesheet
function addToChargesheet(selectedData) {
  // Check if any data is selected
  if (selectedData.length === 0) {
    console.error("No data selected.");
    return;
  }

  // Target the container where chargesheet items will be listed
  var chargesheetList = document.getElementById("chargesheetList");

  // Iterate over each selected data item and create list items for the chargesheet
  selectedData.forEach(function (data) {
    var listItem = document.createElement("li");
    listItem.className = "chargesheet-item";

    // Create and append info divs for each data key-value pair
    for (var key in data) {
      if (data.hasOwnProperty(key)) {
        var infoDiv = createInfoDiv(key, data[key]);
        listItem.appendChild(infoDiv);
      }
    }

    // Create and append a remove button for each chargesheet item
    var removeBtn = createRemoveButton(listItem);
    listItem.appendChild(removeBtn);

    // Append the constructed list item to the chargesheet
    chargesheetList.appendChild(listItem);
  });

  // Deselect the rows in the DataTable after adding them to the chargesheet
  oTable.rows({ selected: true }).deselect();
}

// Function to create a div displaying charge information
function createInfoDiv(key, value) {
  var infoDiv = document.createElement("div");
  infoDiv.className = "charge-info";

  // Span for the key (label)
  var keySpan = document.createElement("span");
  keySpan.className = "charge-key";
  keySpan.textContent = key + ": ";

  // Span for the value
  var valueSpan = document.createElement("span");
  valueSpan.className = "charge-value";
  valueSpan.textContent = value;

  // Append key and value spans to the info div
  infoDiv.appendChild(keySpan);
  infoDiv.appendChild(valueSpan);
  return infoDiv;
}

// Function to create a remove button for a chargesheet item
function createRemoveButton(listItem) {
  var removeBtn = document.createElement("button");
  removeBtn.className = "remove-charge";
  removeBtn.textContent = "Remove";
  // Attach an event handler to remove the chargesheet item on click
  removeBtn.onclick = function () {
    listItem.remove();
  };
  return removeBtn;
}

// Function to export the chargesheet as a PDF
function exportChargesheetAsPDF() {
  // Target the container of the chargesheet
  const chargesheetElement = document.getElementById("chargesheetContainer");

  // Check if the chargesheet container exists
  if (!chargesheetElement) {
    console.error("Chargesheet container element not found.");
    return;
  }

  // Target the row containing buttons
  const buttonRow = document.querySelector(".button-row");

  // Check if the button row exists
  if (!buttonRow) {
    console.error("Button row element not found.");
    return;
  }

  // Temporarily hide the button row while exporting
  buttonRow.classList.add("hidden");

  // Use html2canvas to take a screenshot of the chargesheet and convert it into a PDF
  html2canvas(chargesheetElement)
    .then((canvas) => {
      const imgData = canvas.toDataURL("image/png");
      const pdf = new jsPDF({
        orientation: "portrait",
        unit: "px",
        format: [canvas.width, canvas.height],
      });

      // Add the screenshot image to the PDF
      pdf.addImage(imgData, "PNG", 0, 0, canvas.width, canvas.height);
      // Save the PDF file
      pdf.save("chargesheet.pdf");

      // Show the button row again after exporting
      buttonRow.classList.remove("hidden");
    })
    .catch((err) => {
      console.error("Error exporting PDF:", err);
      // Show the button row again in case of an error
      buttonRow.classList.remove("hidden");
    });
}
