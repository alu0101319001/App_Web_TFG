import subprocess

def execute_ansible_playbook(playbook_path, inventory_path):
    # Construye el comando para ejecutar el playbook de Ansible
    command = [
        'sudo', 'ansible-playbook',
        '-i', inventory_path, playbook_path
    ]

    # Ejecuta el comando y captura la salida
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()

    # Verifica si hubo algún error durante la ejecución del playbook
    if process.returncode != 0:
        # Manejo del error
        print("Error al ejecutar el playbook:")
        print(stderr.decode('utf-8'))
        return stderr.decode('utf-8')
    else:
        # Imprime la salida estándar
        print(stdout.decode('utf-8'))
        return stdout.decode('utf-8')