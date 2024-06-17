import subprocess

def execute_ansible_playbook(playbook_path, inventory_path, extra_vars=None):
    print(f'Executing ansible playbook {playbook_path} with inventory {inventory_path}...')
    command = [
        'sudo', 'ansible-playbook',
        '-i', inventory_path, playbook_path
    ]
    if extra_vars:
        command.append('--extra-vars')
        command.append(extra_vars)

    print(command)

    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    print(f'Processing output...')

    if process.returncode != 0:
        print("Error al ejecutar el playbook:")
        print(stderr.decode('utf-8'))
        return stderr.decode('utf-8')
    else:
        print(stdout.decode('utf-8'))
        return stdout.decode('utf-8')

