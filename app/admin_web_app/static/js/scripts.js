document.addEventListener('DOMContentLoaded', function() {
    const turnOnAllButton = document.getElementById('turnOnAllButton');
    const turnOffAllButton = document.getElementById('turnOffAllButton');
    const updateViewButton = document.getElementById('updateView');

    if (turnOnAllButton) {
        turnOnAllButton.addEventListener('click', function() {
            fetch('/turn-on-all/')
                .then(response => response.text())
                .then(data => {
                    console.log(data);
                    alert("Playbook para encender todos los dispositivos ejecutado correctamente.");
                })
                .catch(error => console.error('Error:', error));
        });
    } else {
        console.log("No turn on button found");
    }

    if (turnOffAllButton) {
        turnOffAllButton.addEventListener('click', function() {
            fetch('/turn-off-all/')
                .then(response => response.text())
                .then(data => {
                    console.log(data);
                    alert("Playbook para apagar todos los dispositivos ejecutado correctamente.");
                })
                .catch(error => console.error('Error:', error));
        });
    } else {
        console.log("No turn off button found");
    }

    if (updateViewButton) {
        updateViewButton.addEventListener('click', function() {
            fetch('/update-view/')
                .then(response => response.text())
                .then(data => {
                    console.log(data);
                    alert("Vista actualizada correctamente.");
                })
                .catch(error => console.error('Error:', error));
        });
    } else {
        console.log("No update view button found");
    }
});


