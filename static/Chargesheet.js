document.addEventListener("DOMContentLoaded", (event) => {
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

async function exportChargesheetAsPDF() {
  const chargesheetElement = document.getElementById("chargesheetContainer");

  if (!chargesheetElement) {
    console.error("Chargesheet container element not found.");
    return;
  }

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
