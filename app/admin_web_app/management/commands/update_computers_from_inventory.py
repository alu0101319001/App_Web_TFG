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

        log[time.time()] = 'Differentiate between sections...'
        # Define las secciones con su estado asociado
        sections = {
            'online': True,
            'offline': False,
            'warning': False,
            'examMode': True
        }

        computers = {section: dict(config.items(section)) if section in config else {} for section in sections}

        for section, computers_list in computers.items():
            state = sections[section]
            log[time.time()] = f'Updating info for {section} computers...'
            for host, details in computers_list.items():
                log[time.time()] = f'\tCalling update for: {host}'
                self.update_computer(host, details, state)

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
        ip = self.get_value_from_string(details, 'ansible_host') if status == True else None

        # Consulta el objeto existente de Computer si está presente
        existing_computer = Computer.objects.filter(mac=mac).first()

        # Determina el valor de warning y examMode según la lógica deseada
        if existing_computer:
            # Si ya existe un registro para esta MAC, mantener el estado actual de warning y resetear el exam_mode
            warning = existing_computer.warning
            exam_mode = False
        else:
            # Si no existe, establece el valor predeterminado de warning y exam_mode
            warning = False  
            exam_mode = False

        # Determina el icono basado en el estado de warning y exam_mode
        if warning:
            icon = 'computer--exclamation.png' # if status == True else 'computer-warning-off.png'
        elif exam_mode and status == True:
            icon = 'computer--pencil.png'
        else:
            icon = 'computer.png' if status == True else 'computer-off.png'

        # Crear o obtener el registro de Computer con los datos actualizados
        computer_defaults = {
            'state': state,
            'ip': ip,
            'icon': icon,
            'warning': warning,  # Mantener el estado actual si no se proporciona explícitamente
            'exam_mode': exam_mode,
        }

        # Actualiza o crea el objeto Computer
        output = f'\tUpdating data: {name}--{state}--{icon}--{mac}--{ip}--{warning}--{exam_mode}'
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
