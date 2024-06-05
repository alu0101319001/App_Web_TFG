#!/bin/bash

# Verificar si se proporciona el argumento de cadena de búsqueda
if [ $# -ne 1 ]; then
    echo "Uso: $0 <cadena>"
    exit 1
fi

# Archivo ethers para usar
ETHER_FILE=../../../../registers/ethers_copy

# Carpeta para almacenar la salida
OUT_DIR=../../../../outputs

# Cadena por la que debe empezar el hostname
SEARCH_STRING="$1"

# Obtener la tabla ARP y resolver el nombre de host para cada IP
arp -a | while read -r line
do
    # Extraer la IP, MAC y nombre de host de cada línea de la salida de arp
    ip=$(echo "$line" | awk '{print $2}' | tr -d '()')
    mac=$(echo "$line" | awk '{print $4}')
    hostname=$(nslookup "$ip" | awk -F 'name = ' '/name = / { print $2 }' | tr -d '.')
    
    # Verificar si el hostname comienza con la cadena de búsqueda
    if [[ "$hostname" == "$SEARCH_STRING"* ]]; then
        # El dispositivo está encendido y encontrado en la tabla ARP
        echo "$hostname $ip $mac on found"
    else
        # Buscar la dirección MAC en el archivo de mapeo ethers
        found=false
        while IFS= read -r ethers_line; do
            ethers_mac=$(echo "$ethers_line" | awk '{print $2}')
            ethers_hostname=$(echo "$ethers_line" | awk '{print $1}')
            if [[ "$mac" == "$ethers_mac" ]]; then
                # El dispositivo está apagado pero encontrado en el archivo de mapeo ethers
                echo "$ethers_hostname $ip $mac off not-found"
                found=true
                break
            fi
        done < "$ETHER_FILE"
    fi
done | sort > "$OUT_DIR/output_scan_"$SEARCH_STRING".txt"
