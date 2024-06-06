import subprocess
import os
import configparser

def generate_ssh_key():
    # Genera una clave SSH en la ruta por defecto
    subprocess.run(['ssh-keygen', '-t', 'rsa', '-N', '', '-f', os.path.expanduser("~/.ssh/id_rsa")])

def add_ssh_key_to_agent():
    # Agrega la clave SSH al agente
    subprocess.run(['ssh-add'])

def copy_ssh_key(host):
    # Copia la clave pública SSH al host remoto
    subprocess.run(['ssh-copy-id', f'administrador@{host}'])

def main():
    # Obtiene la ubicación del directorio actual
    current_dir = os.path.dirname(os.path.abspath(__file__))
    inventory_path = os.path.join(current_dir, '../../../../ansible/inventories/dynamic_inventory.ini')

    # Lee la lista dynamic_inventory.ini
    config = configparser.ConfigParser()
    config.read(inventory_path)
    # Verifica si existe la sección [online]
    if 'online' in config:
        # Extrae las direcciones IP de los hosts del grupo [online]
        online_hosts = config['online']
        online_hosts_ips = [host.split()[0] for host in online_hosts.values() if not host.split()[0].endswith('.33')]
        print(online_hosts_ips)
    else:
        print("No se encontró la sección [online] en el archivo dynamic_inventory.ini")
        return []

    # Genera la clave SSH en la ruta por defecto
    generate_ssh_key()

    # Agrega la clave SSH al agente
    add_ssh_key_to_agent()

    # Copia la clave pública SSH a cada host remoto
    for host in online_hosts_ips:
        copy_ssh_key(host.strip())

if __name__ == "__main__":
    main()
