document.addEventListener('DOMContentLoaded', function() {
    const loadingOverlay = document.getElementById('loadingOverlay');
    const turnOnAllButton = document.getElementById('turnOnAllButton');
    const turnOffAllButton = document.getElementById('turnOffAllButton');
    const runScanButton = document.getElementById('runScanButton');
    const runScriptButton = document.getElementById('runScriptButton');

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

    // Función para mostrar los detalles del ordenador seleccionado
    function showComputerDetails(computerId) {
        // Realizar solicitud al servidor para obtener los detalles del ordenador
        fetch(`/get-computer-details/${computerId}/`)
            .then(response => response.json())
            .then(data => {
                const computerDetailsContainer = document.getElementById('computerDetailsContainer');
                const noComputerSelectedMessage = document.getElementById('noComputerSelectedMessage');
                const computerDetails = document.getElementById('computerDetails');
                
                // Determinar el texto del estado
                const estado = data.state ? "ON" : "OFF";
                const computer_data = encodeURIComponent(JSON.stringify({
                    'name': data.name,
                    'state': estado,
                    'mac': data.mac,
                    'ip': data.ip
                }));
                // Mostrar los detalles del ordenador en el sidebar derecho
                computerDetails.innerHTML = `
                    <p><strong>Nombre:</strong> ${data.name}</p>
                    <p><strong>Estado:</strong> ${estado}</p>
                    <p><strong>MAC:</strong> ${data.mac}</p>
                    <p><strong>IP:</strong> ${data.ip}</p>
                    <!-- Agregar más detalles según sea necesario -->
                    <h5>Opciones</h5>
                    <button class="btn btn-primary" onclick="turnOnComputer('${computer_data}')">Encender</button>
                    <button class="btn btn-primary" onclick="turnOffComputer('${computer_data}')">Apagar</button>
                    <!-- Agregar más botones de opciones según sea necesario -->
                `;

                // Mostrar los detalles del ordenador y ocultar el mensaje "Selecciona un PC"
                noComputerSelectedMessage.style.display = 'none';
                computerDetails.style.display = 'block';
            })
            .catch(error => console.error('Error:', error));
    }

    // Función para encender el ordenador seleccionado
    function turnOnComputer(computerInfoEncoded) {
        const computerInfo = JSON.parse(decodeURIComponent(computerInfoEncoded));
        console.log("Encendiendo el ordenador:", computerInfo.name);
        executePlaybook('up_computers_down.yml', computerInfo.name);    
    }

    // Función para apagar el ordenador seleccionado
    function turnOffComputer(computerInfoEncoded) {
        const computerInfo = JSON.parse(decodeURIComponent(computerInfoEncoded));
        console.log("Apagando el ordenador:", computerInfo.name);
        executePlaybook('down_computers_up.yml', computerInfo.name);
    }

    // Función para ejecutar el playbook de Ansible
    function executePlaybook(playbook, hostname) {
        // Mostrar ventana de carga antes de hacer la solicitud
        showLoadingOverlay(` | Turning On ${hostname} | `);
        fetch(`/execute-playbook/${playbook}/${hostname}/`)
            .then(response => response.text())
            .then(data => {
                console.log(data);
                alert("Playbook para encender el ordenador seleccionado ejecutado correctamente. Espere unos 2 minutos antes de realizar el escaneo.");
            })
            .catch(error => console.error('Error:', error))
            .finally(() => {
                // Ocultar ventana de carga después de que se complete la solicitud
                hideLoadingOverlay();
            });
    }    

    // Función para abrir el explorador de archivos y ejecutar el script seleccionado (con argumento opcional)
    function openFileExplorerAndExecute() {
        const input = document.createElement('input');
        input.type = 'file';
        input.accept = '.sh'; // Aceptar solo archivos con extensión .sh

        input.onchange = function(event) {
            const file = event.target.files[0];
            if (!file) return;

            // Preguntar al usuario si desea ingresar un argumento
            const argument = prompt('Ingrese un argumento para el script (opcional):', '');

            // Llamar a la función para ejecutar el script de bash con el archivo seleccionado y el argumento opcional
            executeShScript(file, argument.trim());
        };

        input.click(); // Abrir el explorador de archivos
    }

    // Función para ejecutar el script de bash seleccionado (con argumento opcional)
    function executeShScript(scriptFile, argument) {
        // Mostrar ventana de carga antes de hacer la solicitud
        showLoadingOverlay('Running .sh Script');

        const formData = new FormData();
        formData.append('scriptFile', scriptFile);
        if (argument) {
            formData.append('argument', argument); // Agregar el argumento al FormData solo si está presente
        }

        fetch('/run-sh-script/', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            console.log('Script execution result:', data.output);
            alert('Script executed successfully.'); // Puedes ajustar el mensaje de alerta según necesites
        })
        .catch(error => console.error('Error:', error))
        .finally(() => {
            // Ocultar ventana de carga después de que se complete la solicitud
            hideLoadingOverlay();
        });
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
                    }, 1000);
                })
                .catch(error => console.error('Error:', error))
                .finally(() => {
                    // Ocultar ventana de carga después de que se complete la solicitud
                    hideLoadingOverlay();
                });
        });
    }

    if (runScriptButton) {
        runScriptButton.addEventListener('click', openFileExplorerAndExecute);
    }
});
