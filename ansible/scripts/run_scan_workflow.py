import subprocess
import os

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
VENV_PATH = "/home/administrador/Documentos/Repositorios/tfg_app_web_proyecto/venv"
PROJECT_PATH = "/home/administrador/Documentos/Repositorios/tfg_app_web_proyecto"

def run_external_script(script_path):
    try:
        # Crea un script bash temporal para activar el entorno virtual, establecer PYTHONPATH y ejecutar el script Python
        bash_script = f"""
        #!/bin/bash
        source {VENV_PATH}/bin/activate
        export PYTHONPATH={PROJECT_PATH}:${{PYTHONPATH}}        
        python3.12 {script_path}
        """
        bash_script_path = os.path.join(CURRENT_DIR, 'run_script.sh')
        
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
    scan_yml_path = "/home/administrador/Documentos/Repositorios/tfg_app_web_proyecto/ansible/playbooks/scan_p1_19_lab.yml"
    update_yml_path = "/home/administrador/Documentos/Repositorios/tfg_app_web_proyecto/ansible/playbooks/update_inventory.yml"

    commands = [
        f"sudo ansible-playbook -vvv {scan_yml_path}",
        f"sudo ansible-playbook -vvv {update_yml_path}"
    ]

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
            break

def run_scan_update():
    # Ejecutar otro script de Python
    script_path = os.path.abspath(os.path.join(CURRENT_DIR, '../../app/admin_web_app/management/commands/update_computers_from_inventory.py'))
    output = run_external_script(script_path)
    print("Script output:", output)

# Llama a la función para ejecutar los comandos
run_scan_playbook()
run_scan_update()
