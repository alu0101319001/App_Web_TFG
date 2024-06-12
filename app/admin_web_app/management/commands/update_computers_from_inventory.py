import os
from io import StringIO
from django.core.management.base import BaseCommand
from admin_web_app.models import Computer
import configparser

class Command(BaseCommand):
    help = 'Update computers from Ansible inventory'

    def handle(self, *args, **kwargs):
        # Define la ruta del archivo de inventario como constante
        current_dir = os.path.dirname(os.path.abspath(__file__))
        inventory_path = os.path.join(current_dir, '../../../../ansible/inventories/dynamic_inventory.ini')

        # Parsea el archivo dynamic_inventory.ini
        config = configparser.ConfigParser()
        config.read(inventory_path)

        # Obtén la sección 'online' del inventario
        online_computers = {}
        if 'online' in config:
            online_computers = dict(config.items('online'))

        # Obtén la sección 'offline' del inventario
        offline_computers = {}
        if 'offline' in config:
            offline_computers = dict(config.items('offline'))

        # Limpiar la base de datos de ordenadores existentes
        Computer.objects.all().delete()

        # Iterar sobre los ordenadores en línea y actualizar la base de datos
        for host, details in online_computers.items():
            self.update_computer(host, details, 'online')

        # Iterar sobre los ordenadores fuera de línea y actualizar la base de datos
        for host, details in offline_computers.items():
            self.update_computer(host, details, 'offline')

        return "Computers updated successfully."

    def update_computer(self, host, details, status):
        name = host.split()[0]
        state = self.get_value_from_string(details, 'status')
        mac = self.get_value_from_string(details, 'mac_address')
        
        # Obtén la dirección IP solo si el estado es "online"
        ip = self.get_value_from_string(details, 'ansible_host') if status.lower() == 'online' else None
        icon = 'computer.png' if status.lower() == 'online' else 'computer-off.png'

        # Insertar o actualizar el registro en la base de datos
        computer = Computer(name=name, state=state, icon=icon, mac=mac, ip=ip)
        computer.save()
        return f"Inventory computers created successfully for {name}."

    def get_value_from_string(self, string, key):
        # Parsea el valor de la cadena para obtener el valor de la clave especificada
        if key + '=' in string:
            parts = string.split(key + '=')
            if len(parts) > 1:
                return parts[1].split()[0]
        elif key == 'ansible_host':
            # Si la clave 'ansible_host' no está presente, devuelve None
            return string.split()[0]
        else:
            return None
