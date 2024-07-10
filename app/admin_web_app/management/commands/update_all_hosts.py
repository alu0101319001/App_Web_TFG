import os
import configparser
from django.core.management.base import BaseCommand
from admin_web_app.models import Computer

class Command(BaseCommand):
    help = 'Update all computers in the inventory and the computer database based on a scan output file'

    def handle(self, *args, **kwargs):
        output_file = os.path.expanduser('~/Documentos/Repositorios/tfg_app_web_proyecto/outputs/output_scan_p1-019-.txt')
        if not os.path.exists(output_file):
            self.stdout.write(f"No output file found at {output_file}")
            return

        inventory_path = os.path.expanduser('~/Documentos/Repositorios/tfg_app_web_proyecto/ansible/inventories/dynamic_inventory.ini')
        config = configparser.ConfigParser()
        config.read(inventory_path)

        # Ensure all necessary sections exist
        for section in ['online', 'offline', 'warning', 'examMode']:
            if not config.has_section(section):
                config.add_section(section)

        with open(output_file, 'r') as file:
            for line in file:
                hostname, mac, ip, status_str = line.strip().split()
                status = status_str == 'on'
                self.update_inventory_file(config, hostname, mac, ip, status)

        # Write the updated inventory back to the file
        with open(inventory_path, 'w') as configfile:
            config.write(configfile)

        # Update the database
        with open(output_file, 'r') as file:
            for line in file:
                hostname, mac, ip, status_str = line.strip().split()
                status = status_str == 'on'
                self.update_computer_database(hostname, mac, ip, status)

    def update_inventory_file(self, config, host, mac, ip, status):
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

        # Remove host from all possible sections first
        for sec in ['online', 'offline', 'warning', 'examMode']:
            if config.has_section(sec) and config.has_option(sec, host):
                config.remove_option(sec, host)

        # Now place the host in the appropriate section based on status
        config.set(section, host, f"ansible_host={ip} mac_address={mac} status={status} warning={warning} exam_mode={exam_mode}")

        self.stdout.write(f"Inventario actualizado para {host} en la sección {section}")

    def update_computer_database(self, host, mac, ip, status):
        try:
            computer = Computer.objects.get(mac=mac)
            warning = computer.warning
            exam_mode = computer.exam_mode
        except Computer.DoesNotExist:
            warning = False
            exam_mode = False

        # Determine the icon based on the state
        if warning:
            icon = 'computer--exclamation.png'
        elif not status:
            icon = 'computer-off.png'
            exam_mode = False
        elif exam_mode and status:
            icon = 'computer--pencil.png'
        else:
            icon = 'computer.png'

        # Create or update the Computer record
        computer_defaults = {
            'state': status,
            'ip': ip if status else None,
            'icon': icon,
            'warning': warning,
            'exam_mode': exam_mode,
        }

        output = f'\tUpdating data: {host}--{status}--{icon}--{mac}--{ip}--{warning}--{exam_mode}'
        Computer.get_or_create_by_name_and_mac(host, mac, computer_defaults)
        output += f'\n\tInventory computers created successfully for {host}'
        self.stdout.write(output)

    def get_value_from_string(self, string, key):
        # Parse the value from the string to get the specified key
        if key + '=' in string:
            parts = string.split(key + '=')
            if len(parts) > 1:
                return parts[1].split()[0]
        elif key == 'ansible_host':
            # If the key 'ansible_host' is not present, return None
            return string.split()[0]
        else:
            return None
