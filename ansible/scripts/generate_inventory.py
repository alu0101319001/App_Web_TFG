import json
import os

# Ruta del archivo de salida del escaneo
output_file = os.path.expanduser('~/Documentos/Repositorios/tfg_app_web_proyecto/outputs/output_scan_p1-019-.txt')
inventory = {
    "all": {
        "hosts": [],
        "children": {}
    }
}

with open(output_file, 'r') as f:
    for line in f:
        parts = line.strip().split()
        hostname, mac, ip, status = parts[0], parts[1], parts[2], parts[3]
        inventory['all']['hosts'].append({
            'hostname': hostname,
            'ansible_host': ip,
            'mac_address': mac,
            'status': status  # Agregar el estado del host al inventario
        })

# Imprimir el inventario en formato JSON
print(json.dumps(inventory, indent=2))
