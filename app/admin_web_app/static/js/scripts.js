document.addEventListener('DOMContentLoaded', function() {
    const loadingOverlay = document.getElementById('loadingOverlay');
    const turnOnAllButton = document.getElementById('turnOnAllButton');
    const turnOffAllButton = document.getElementById('turnOffAllButton');
    const runScanButton = document.getElementById('runScanButton');

    function showLoadingOverlay(name_function=null) {
        const loadingMessage = document.getElementById('loadingMessage');
        loadingMessage.textContent = name_function ? `Executing ${name_function}...` : 'Executing funcionality...';
    
        const loadingOverlay = document.getElementById('loadingOverlay');
        loadingOverlay.style.display = 'block';
    }
    
    function hideLoadingOverlay() {
        const loadingOverlay = document.getElementById('loadingOverlay');
        loadingOverlay.style.display = 'none';
    }

    if (turnOnAllButton) {
        turnOnAllButton.addEventListener('click', function() {
            // Mostrar ventana de carga antes de hacer la solicitud
            showLoadingOverlay(' | Turning On All PCs | ');

            fetch('/turn-on-all/')
                .then(response => response.text())
                .then(data => {
                    console.log(data);
                    alert("Playbook para encender todos los dispositivos ejecutado correctamente. Espere unos 2 minutos antes de realizar el escaneo.");
                })
                .catch(error => console.error('Error:', error))
                .finally(() => {
                    // Ocultar ventana de carga después de que se complete la solicitud
                    hideLoadingOverlay();
                });
        });
    } else {
        console.log("No turn on button found");
    }

    if (turnOffAllButton) {
        turnOffAllButton.addEventListener('click', function() {
            // Mostrar ventana de carga antes de hacer la solicitud
            showLoadingOverlay(' | Turning OFF All PCs | ');

            fetch('/turn-off-all/')
                .then(response => response.text())
                .then(data => {
                    console.log(data);
                    alert("Playbook para apagar todos los dispositivos ejecutado correctamente. Espere unos 2 minutos antes de realizar el escaneo.");
                })
                .catch(error => console.error('Error:', error))
                .finally(() => {
                    // Ocultar ventana de carga después de que se complete la solicitud
                    hideLoadingOverlay();
                });
        });
    } else {
        console.log("No turn off button found");
    }

    if (runScanButton) {
        runScanButton.addEventListener('click', function() {
            // Mostrar ventana de carga antes de hacer la solicitud
            showLoadingOverlay(' | Scanning PC Laboratory | ');
    
            // Lógica para ejecutar el escaneo
            fetch('/run-scan/')
                .then(response => response.json())
                .then(data => {
                    console.log('Playbook result:', data.playbook_result);
                    console.log('Update result:', data.update_result);
                    alert("Scan executed successfully."); // Actualiza el mensaje de alerta si lo deseas
    
                    // Redireccionar después de 2 segundos
                    setTimeout(function() {
                        window.location.reload();
                    }, 2000);
                })
                .catch(error => console.error('Error:', error))
                .finally(() => {
                    // Ocultar ventana de carga después de que se complete la solicitud
                    hideLoadingOverlay();
                });
        });
    }
});
