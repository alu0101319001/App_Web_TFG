from django.http import HttpResponse
from django.conf import settings
from django.core.management import execute_from_command_line
import subprocess
import os
import io
import sys
import time

# Añade el directorio del proyecto al PYTHONPATH
sys.path.append(settings.BASE_DIR)

def run_external_script(script_path):
    try:
        # Crea un script bash temporal para activar el entorno virtual, establecer PYTHONPATH y ejecutar el script Python
        bash_script = f"""
        #!/bin/bash
        source {settings.VENV_PATH}/bin/activate
        export PYTHONPATH={settings.PROJECT_PATH}:${{PYTHONPATH}}
        python3.12 {script_path}
        """
        bash_script_path = os.path.join(settings.BASE_DIR, 'run_script.sh')
        
        # Guarda el script bash en un archivo temporal
        with open(bash_script_path, 'w') as file:
            file.write(bash_script)
        
        # Asegúrate de que el script bash tenga permisos de ejecución
        os.chmod(bash_script_path, 0o755)

        # Ejecuta el script bash con sudo usando bash explícitamente
        command = ['sudo', 'bash', bash_script_path]

        # Ejecuta el script y captura la salida
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()

        # Elimina el script bash temporal
        os.remove(bash_script_path)

        # Verifica si la ejecución fue exitosa
        if process.returncode == 0:
            # Devuelve la salida decodificada del stdout
            return stdout.decode('utf-8')
        else:
            # Devuelve la salida de error decodificada en caso de error
            return stderr.decode('utf-8')
    except Exception as e:
        # Maneja excepciones y devuelve un mensaje de error
        return f"Error al ejecutar el script externo: {e}"

def run_scan_playbook():
    scan_yml_path = os.path.join(settings.PROJECT_PATH, "ansible", "playbooks", "scan_p1_19_lab.yml")
    update_yml_path = os.path.join(settings.PROJECT_PATH, "ansible", "playbooks", "update_inventory.yml")

    commands = [
        f"sudo ansible-playbook {scan_yml_path}",
        f"sudo ansible-playbook {update_yml_path}"
    ]

    result_list = []
    for command in commands:
        result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout = result.stdout.decode('utf-8')
        stderr = result.stderr.decode('utf-8')
        
        print(f"Executing command: {command}")
        print("Output:", stdout)
        if result.returncode != 0:
            print("Error executing command:", command)
            print("Error Output:", stderr)
            print("Return code:", result.returncode)
            result_list.append(f"Error executing command: {command}\nError Output: {stderr}\nReturn code: {result.returncode}")
        else:
            result_list.append(stdout)
    
    return result_list

def run_scan_update():
    script_path = os.path.join(settings.BASE_DIR, 'admin_web_app', 'management', 'commands', 'update_computers_from_inventory.py')
    
    # Capturar la salida del script en objetos StringIO
    stdout_capture = io.StringIO()
    stderr_capture = io.StringIO()

    # Redirigir la salida estándar y la salida de error al objeto StringIO
    sys.stdout = stdout_capture
    sys.stderr = stderr_capture

    try:
        # Ejecutar el script
        execute_from_command_line(['manage.py', 'update_computers_from_inventory'])
    finally:
        # Restaurar la salida estándar y la salida de error
        sys.stdout = sys.__stdout__
        sys.stderr = sys.__stderr__

    # Obtener la salida del objeto StringIO
    stdout_output = stdout_capture.getvalue()
    stderr_output = stderr_capture.getvalue()

     # Procesar la salida para crear una cadena de log
    log_output = stdout_output
    if stderr_output:
        log_output += f"\nError: {stderr_output}"

    return log_output

