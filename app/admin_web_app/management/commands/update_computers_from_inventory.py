# admin_web_app/management/commands/update_computers.py
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
            self.update_computer(host, details, 'online')
        
        # Iterar sobre los ordenadores fuera de línea y actualizar la base de datos
        log[time.time()] = 'Updating info for offline computers...'
        for host, details in offline_computers.items():
            log[time.time()] = f'\tCalling update for: {host}'
            self.update_computer(host, details, 'offline')

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

        # Consulta el objeto existente de Computer si está presente
        existing_computer = Computer.objects.filter(mac=mac).first()

        # Determina el valor de warning según la lógica deseada
        if existing_computer:
            # Si ya existe un registro para esta MAC, mantener el estado actual de warning
            warning = existing_computer.warning
        else:
            # Si no existe, establece el valor predeterminado de warning
            warning = False  # Ajusta esto según tu lógica inicial

        # Determina el icono basado en el estado de warning
        if warning:
            icon = 'computer--exclamation.png' # if status.lower() == 'online' else 'computer-warning-off.png'
        else:
            icon = 'computer.png' if status.lower() == 'online' else 'computer-off.png'

        # Crear o obtener el registro de Computer con los datos actualizados
        computer_defaults = {
            'state': state,
            'ip': ip,
            'icon': icon,
            'warning': warning,  # Mantener el estado actual si no se proporciona explícitamente
        }

        # Actualiza o crea el objeto Computer
        output = f'\tUpdating data: {name}--{state}--{icon}--{mac}--{ip}'
        Computer.get_or_create_by_name_and_mac(name, mac, computer_defaults)
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
