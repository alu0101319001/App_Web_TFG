import subprocess

def run_scan_playbook():
    commands = [
        "ansible-playbook -vvv ../playbooks/scan_p1_19_lab.yml --ask-become-pass",
        "ansible-playbook ../playbooks/update_inventory.yml"
    ]

    for command in commands:
        result = subprocess.run(command, shell=True)
        if result.returncode != 0:
            print("Error executing command:", command)
            print("Return code:", result.returncode)
            break

# Llama a la función para ejecutar los comandos
run_scan_playbook()
