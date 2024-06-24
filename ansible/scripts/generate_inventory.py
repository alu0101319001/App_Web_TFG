import os
import sys
import django

# Añadir la ruta al directorio principal del proyecto Django al sys.path
proyecto_django_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../app/'))
sys.path.append(proyecto_django_dir)

# Configura Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'admin_web_project_dj.settings')
django.setup()

from admin_web_app.models import Computer

# Ruta del archivo de salida del escaneo
output_file = os.path.expanduser('~/Documentos/Repositorios/tfg_app_web_proyecto/outputs/output_scan_p1-019-.txt')
inventory = {}

with open(output_file, 'r') as f:
    for line in f:
        parts = line.strip().split()
        hostname, mac, ip, status = parts[0], parts[1], parts[2], parts[3]
        # Consultar la base de datos para obtener warning y examMode
        try:
            computer = Computer.objects.get(mac=mac)
            warning = computer.warning
            exam_mode = computer.exam_mode  # Asegúrate de que el campo se llame exam_mode en tu modelo
        except Computer.DoesNotExist:
            warning = False  # Valor predeterminado si no se encuentra
            exam_mode = False  # Valor predeterminado si no se encuentra
        
        inventory[hostname] = {
            'ansible_host': ip,
            'mac_address': mac,
            'status': status,
            'warning': warning,
            'exam_mode': exam_mode
        }

# Imprimir el inventario en formato YAML
for host, info in inventory.items():
    print(f"{host}:")
    for key, value in info.items():
        print(f"  {key}: {value}")
