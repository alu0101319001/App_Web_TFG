from ansible_runner import run

def run_playbook():
    result = run(playbook='ansible/playbooks/scan_network.yml', inventory='ansible/inventories/production.ini')
    if result.rc != 0:
        print("Error executing playbook:", result.rc)

# Llama a la función para ejecutar el playbook
run_playbook()
