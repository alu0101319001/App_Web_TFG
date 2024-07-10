import subprocess
import os
import io
import sys
import time
import re
import json
from django.http import HttpResponse
from django.conf import settings
from django.core.management import execute_from_command_line
from .models import Computer


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

    commands = [
        f"sudo ansible-playbook -vvv {scan_yml_path}"
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
    script_path = os.path.join(settings.BASE_DIR, 'admin_web_app', 'management', 'commands', 'update_all_hosts.py')
    
    # Capturar la salida del script en objetos StringIO
    stdout_capture = io.StringIO()
    stderr_capture = io.StringIO()

    # Redirigir la salida estándar y la salida de error al objeto StringIO
    sys.stdout = stdout_capture
    sys.stderr = stderr_capture

    try:
        # Ejecutar el script
        execute_from_command_line(['manage.py', 'update_all_hosts'])
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

def run_single_scan_update(hostname):
    script_path = os.path.join(settings.BASE_DIR, 'admin_web_app', 'management', 'commands', 'update_single_host.py')
    
    # Capturar la salida del script en objetos StringIO
    stdout_capture = io.StringIO()
    stderr_capture = io.StringIO()

    # Redirigir la salida estándar y la salida de error al objeto StringIO
    sys.stdout = stdout_capture
    sys.stderr = stderr_capture

    try:
        # Ejecutar el script
        execute_from_command_line(['manage.py', 'update_single_host', hostname])
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

def run_copyFiles_playbook(folder, files):
    copyFiles_yml_path = os.path.join(settings.PROJECT_PATH, "ansible", "playbooks", "copyFiles.yml")
    inventory_path = os.path.join(settings.PROJECT_PATH, "ansible", "inventories", "dynamic_inventory.ini")

    command = [
        'ansible-playbook',
        copyFiles_yml_path,
        '-i', inventory_path,
        '--extra-vars', f'folder={folder} files={files}'
    ]

    try:
        # Ejecutar el playbook
        subprocess.run(command, check=True)

        # Leer el contenido del archivo temporal
        temp_file_path = "/tmp/ansible_summary_message.txt"
        if os.path.exists(temp_file_path):
            with open(temp_file_path, 'r') as f:
                summary_message = f.read().strip()
                return {'summary_message': summary_message}
        else:
            return {'error': 'Summary message file not found'}

    except subprocess.CalledProcessError as e:
        return {'error': f'An error occurred: {e}'}

def update_exam_mode_and_icon_for_online_computers(new_exam_mode, new_icon):
    # Obtiene todas las computadoras con estado True
    online_computers = Computer.objects.filter(state=True)
    
    # Extrae las IDs de las computadoras
    computer_ids = list(online_computers.values_list('id', flat=True))
    
    # Actualiza el estado de exam_mode y el icono para todas las computadoras en línea
    for computer in online_computers:
        computer.exam_mode = new_exam_mode
        computer.icon = new_icon
        computer.save()

    return computer_ids

