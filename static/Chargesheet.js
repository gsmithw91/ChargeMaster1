// Listen for the DOMContentLoaded event to ensure the DOM is fully loaded before executing the script
document.addEventListener("DOMContentLoaded", (event) => {
<<<<<<< HEAD
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
=======
  // Listener for the "Export as PDF" button click
  var exportPdfButton = document.getElementById("exportPdfButton");
  if (exportPdfButton) {
    exportPdfButton.addEventListener("click", function () {
      exportChargesheetAsPDF()
        .then(() => console.log("PDF export successful"))
        .catch((error) => console.error("PDF export error:", error));
    });
  }

  // Listener for the "Process Selections" button click
  var sendDataButton = document.getElementById("sendDataButton");
  if (sendDataButton) {
    sendDataButton.addEventListener("click", sendChargeSheetData);
  }
});

const exportPdfButton = document.getElementById("exportPdfButton");
if (exportPdfButton) {
  exportPdfButton.addEventListener("click", () => exportChargesheetAsPDF());
}

const clearChargesButton = document.getElementById("clearChargesButton");
if (clearChargesButton) {
  clearChargesButton.addEventListener("click", clearChargesheet);
}

// Add this section for sending the chargesheet data
const sendDataButton = document.getElementById("sendDataButton");
if (sendDataButton) {
  sendDataButton.addEventListener("click", sendChargeSheetData);
}

function clearChargesheet() {
  if (confirm("Are you sure you want to clear the chargesheet?")) {
    var chargesheetList = document.getElementById("chargesheetList");
    chargesheetList.innerHTML = "";
  }
>>>>>>> 5b6a4a5c8e0f33cdde4ef2008b98d3c9b85947a2
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

<<<<<<< HEAD
// Function to export the chargesheet as a PDF
function exportChargesheetAsPDF() {
  // Target the container of the chargesheet
  const chargesheetElement = document.getElementById("chargesheetContainer");

  // Check if the chargesheet container exists
=======
async function exportChargesheetAsPDF() {
  const chargesheetElement = document.getElementById("chargesheetContainer");

>>>>>>> 5b6a4a5c8e0f33cdde4ef2008b98d3c9b85947a2
  if (!chargesheetElement) {
    console.error("Chargesheet container element not found.");
    return;
  }

<<<<<<< HEAD
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
=======
  // Create an instance of jsPDF
  const pdf = new jsPDF({
    orientation: "portrait",
    unit: "px",
  });

  // Use html2canvas to capture the chargesheetElement as an image
  const canvas = await html2canvas(chargesheetElement);
  const imgData = canvas.toDataURL("image/png");
  const imgWidth = 210; // mm (A4 width)
  const imgHeight = (canvas.height * imgWidth) / canvas.width;

  pdf.addImage(imgData, "PNG", 0, 0, imgWidth, imgHeight);
  pdf.save("chargesheet.pdf");
}
async function sendChargeSheetData() {
  // Check if the chargesheetList element exists
  var chargesheetList = document.getElementById("chargesheetList");
  if (!chargesheetList) {
    console.error("Element with id 'chargesheetList' not found.");
    return;
  }

  // Select all chargesheet-item elements within chargesheetList
  var chargesheetItems = chargesheetList.querySelectorAll(".chargesheet-item");

  var dataToSend = Array.from(chargesheetItems).map((item) => {
    var data = {};

    // Check if charge-info elements exist within the current chargesheet-item
    var chargeInfoDivs = item.querySelectorAll(".charge-info");
    if (!chargeInfoDivs.length) {
      console.error(
        "No '.charge-info' elements found within a chargesheet-item."
      );
      return;
    }

    chargeInfoDivs.forEach((infoDiv) => {
      // Check if charge-key and charge-value elements exist within charge-info
      var chargeKey = infoDiv.querySelector(".charge-key");
      var chargeValue = infoDiv.querySelector(".charge-value");

      if (chargeKey && chargeValue) {
        var key = chargeKey.textContent.replace(": ", "");
        var value = chargeValue.textContent;
        data[key] = value;
      } else {
        console.error(
          "Incomplete charge-info structure within a chargesheet-item."
        );
      }
>>>>>>> 5b6a4a5c8e0f33cdde4ef2008b98d3c9b85947a2
    });
    return data;
  });

  try {
    const response = await fetch("/api/process-chargesheet", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(dataToSend),
    });

    if (response.ok) {
      const responseData = await response.json();
      // Open the response URL in a new window/tab
      window.open(responseData.redirect_url, "_blank");
    } else {
      console.error("Failed to send chargesheet data.");
    }
  } catch (error) {
    console.error("Error sending chargesheet data:", error);
  }
}
