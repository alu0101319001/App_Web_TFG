import os
import time
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

        # Registra un log
        log = {}

        # Parsea el archivo dynamic_inventory.ini
        log[time.time()] = 'Parsing dynamic_inventory.ini...'
        config = configparser.ConfigParser()
        config.read(inventory_path)

        log[time.time()] = 'Differentiate between online and offline sections...'
        # Obtén la sección 'online' del inventario
        online_computers = {}
        if 'online' in config:
            online_computers = dict(config.items('online'))

        # Obtén la sección 'offline' del inventario
        offline_computers = {}
        if 'offline' in config:
            offline_computers = dict(config.items('offline'))

        # Iterar sobre los ordenadores en línea y actualizar la base de datos
        log[time.time()] = 'Updating info for online computers...'
        for host, details in online_computers.items():
            log[time.time()] = f'\tCalling update for: {host}'
            output = self.update_computer(host, details, 'online')
            log[time.time()] = output

        # Iterar sobre los ordenadores fuera de línea y actualizar la base de datos
        log[time.time()] = 'Updating info for offline computers...'
        for host, details in offline_computers.items():
            log[time.time()] = f'\tCalling update for: {host}'
            output = self.update_computer(host, details, 'offline')
            log[time.time()] = output

        log[time.time()] = 'Computers updated successfully.\nEND'
        sorted_log = dict(sorted(log.items()))

        # Convertir el diccionario de log a una cadena
        log_string = "\n".join([f"{time.ctime(timestamp)}: {message}" for timestamp, message in sorted_log.items()])
        
        return log_string

    def update_computer(self, host, details, status):
        name = host.split()[0]
        state = self.get_value_from_string(details, 'status')
        mac = self.get_value_from_string(details, 'mac_address')
        
        # Obtén la dirección IP solo si el estado es "online"
        ip = self.get_value_from_string(details, 'ansible_host') if status.lower() == 'online' else None

        # Busca si existe un registro con la misma MAC
        existing_computer = Computer.objects.filter(mac=mac).first()
        if existing_computer:
            # Si existe, mantén el valor de warning y asigna el icono correspondiente
            warning = existing_computer.warning
            icon = 'computer--exclamation.png' if warning else ('computer.png' if status.lower() == 'online' else 'computer-off.png')
        else:
            # Si no existe, asigna el icono predeterminado
            warning = False
            icon = 'computer.png' if status.lower() == 'online' else 'computer-off.png'

        # Insertar o actualizar el registro en la base de datos
        output = f'\tUpdating data: {name}--{state}--{icon}--{mac}--{ip}'
        computer = Computer(name=name, state=state, icon=icon, mac=mac, ip=ip, warning=warning)
        computer.save()
        output += f'\n\tInventory computers created successfully for {name}'
        return output

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
