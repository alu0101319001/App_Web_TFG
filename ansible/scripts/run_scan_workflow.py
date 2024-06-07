import subprocess
import os

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))

def run_scan_playbook():
    commands = [
        "sudo ansible-playbook -vvv ../playbooks/scan_p1_19_lab.yml",
        "sudo ansible-playbook ../playbooks/update_inventory.yml"
    ]

    for command in commands:
        result = subprocess.run(command, shell=True)
        if result.returncode != 0:
            print("Error executing command:", command)
            print("Return code:", result.returncode)
            break

def run_scan_update():
    # Ejecutar otro script de Python
    script_path = os.path.abspath(os.path.join(CURRENT_DIR, '../../app/admin_web_app/management/commands/update_computers_from_inventory.py'))
    python_script_command = f"sudo python3.12 {script_path}"
    python_script_result = subprocess.run(python_script_command, shell=True)
    if python_script_result.returncode != 0:
        print("Error executing Python script:", python_script_command)
        print("Return code:", python_script_result.returncode)

# Llama a la función para ejecutar los comandos
run_scan_playbook()
run_scan_update()
