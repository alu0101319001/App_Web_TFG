import os
import configparser
from django.core.management.base import BaseCommand
from admin_web_app.models import Computer

class Command(BaseCommand):
    help = 'Updates a single host in the inventory and the computer database based on specific conditions'

    def add_arguments(self, parser):
        # Define the single argument this command will take: the hostname
        parser.add_argument('host', type=str, help="Host name of the computer to be updated")

    def handle(self, *args, **options):
        host = options['host']
        self.stdout.write(f"Updating inventory and database for host: {host}")
        self.update_single_host_inventory(host)
        self.update_computer_database(host)

    def update_single_host_inventory(self, target_host):
        output_file = os.path.expanduser(f'~/Documentos/Repositorios/tfg_app_web_proyecto/outputs/scan_for_hosts/output_scan_{target_host}.txt')
        if not os.path.exists(output_file):
            self.stdout.write(f"No output file found for {target_host}")
            return

        with open(output_file, 'r') as file:
            for line in file:
                hostname, mac, ip, status_str = line.strip().split()
                status = status_str == 'on'
                self.update_inventory_file(hostname, mac, ip, status)

    def update_inventory_file(self, host, mac, ip, status):
        try:
            computer = Computer.objects.get(mac=mac)
            warning = computer.warning
            exam_mode = computer.exam_mode
        except Computer.DoesNotExist:
            warning = False
            exam_mode = False

        # Determine the correct section based on the computer's status
        if warning:
            section = 'warning'
        elif not status:
            section = 'offline'
        elif exam_mode:
            section = 'examMode'
        else:
            section = 'online'

        inventory_path = os.path.expanduser('~/Documentos/Repositorios/tfg_app_web_proyecto/ansible/inventories/dynamic_inventory.ini')
        config = configparser.ConfigParser()
        config.read(inventory_path)

        # Ensure the section exists
        if not config.has_section(section):
            config.add_section(section)

        # Remove host from all possible sections first
        for sec in ['online', 'offline', 'warning', 'examMode']:
            if config.has_section(sec) and config.has_option(sec, host):
                config.remove_option(sec, host)

        # Now place the host in the appropriate section based on status
        config.set(section, host, f"ansible_host={ip} mac_address={mac} status={status} warning={warning} exam_mode={exam_mode}")

        # Write changes back to the inventory file
        with open(inventory_path, 'w') as configfile:
            config.write(configfile)

        self.stdout.write(f"Inventario actualizado para {host} en la sección {section}")

    def update_computer_database(self, target_host):
        inventory_path = os.path.expanduser('~/Documentos/Repositorios/tfg_app_web_proyecto/ansible/inventories/dynamic_inventory.ini')
        config = configparser.ConfigParser()
        config.read(inventory_path)

        # Find the host in the inventory file
        for section in config.sections():
            if config.has_option(section, target_host):
                host_info = config.get(section, target_host)
                break
        else:
            self.stdout.write(f"No inventory entry found for host: {target_host}")
            return

        # Update the computer in the database
        output = self.update_computer(target_host, host_info, self.get_value_from_string(host_info, 'status') == 'True')
        self.stdout.write(output)

    def update_computer(self, host, details, status):
        name = host.split()[0]
        state = self.get_value_from_string(details, 'status')
        mac = self.get_value_from_string(details, 'mac_address')
        
        # Obtén la dirección IP solo si el estado es "online"
        ip = self.get_value_from_string(details, 'ansible_host') if status else None

        # Consulta el objeto existente de Computer si está presente
        existing_computer = Computer.objects.filter(mac=mac).first()

        # Determina el valor de warning y exam_mode según la lógica deseada
        if existing_computer:
            # Si ya existe un registro para esta MAC, mantener el estado actual de warning y resetear el exam_mode
            warning = existing_computer.warning
            exam_mode = existing_computer.exam_mode
        else:
            # Si no existe, establece el valor predeterminado de warning y exam_mode
            warning = False  
            exam_mode = False

        # Determina el icono basado en el estado de warning y exam_mode
        if warning:
            icon = 'computer--exclamation.png'
        elif not status:
            icon = 'computer-off.png'
            exam_mode = False
        elif exam_mode and status:
            icon = 'computer--pencil.png'
        else:
            icon = 'computer.png' 

        # Crear o obtener el registro de Computer con los datos actualizados
        computer_defaults = {
            'state': state,
            'ip': ip,
            'icon': icon,
            'warning': warning,
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
