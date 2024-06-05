//static/js/scripts.js
document.addEventListener('DOMContentLoaded', function() {
  console.log("DOM fully loaded and parsed");
  const openButtons = document.querySelectorAll(".btn-open-computer-info");
  const modal = document.getElementById("computerModal");
  const modalName = document.getElementById("modalName");
  const modalStatus = document.getElementById("modalStatus");
  const closeModalButton = document.getElementById("btn-close-computer-info");

  if (openButtons.length > 0) {
      console.log("Found open buttons:", openButtons.length);
  } else {
      console.log("No open buttons found");
  }

  openButtons.forEach(button => {
      console.log("Adding event listener to button", button);
      button.addEventListener("click", function() {
          console.log("Button clicked");
          const name = this.getAttribute("data-name");
          const status = this.getAttribute("data-status");
          console.log("Opening modal for:", name, status);
          modalName.textContent = name;
          modalStatus.textContent = status;
          modal.showModal();
      });
  });

  closeModalButton.addEventListener("click", function() {
      console.log("Closing modal");
      modal.close();
  });
});



