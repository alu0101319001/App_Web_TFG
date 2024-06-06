#!/bin/bash

# Verificar si se proporciona el argumento de cadena de búsqueda
if [ $# -ne 1 ]; then
    echo "Uso: $0 <cadena>"
    exit 1
fi

# Establecer rutas y nombres de archivos
PROJECT_DIR="$HOME/Documentos/Repositorios/tfg_app_web_proyecto"
ETHER_FILE="$PROJECT_DIR/registers/ethers_copy"
OUT_DIR="$PROJECT_DIR/outputs"

# Cadena por la que debe empezar el hostname
SEARCH_STRING="$1"

# Imprimir mensaje de depuración
echo "Cadena de búsqueda: $SEARCH_STRING"

# Obtener la tabla ARP y crear un diccionario de MAC a IP
declare -A arp_table
while read -r line; do
    mac=$(echo "$line" | awk '{print $4}')
    ip=$(echo "$line" | awk '{print $2}' | tr -d '()')
    arp_table["$mac"]="$ip"
    echo "arp_table['$mac']=$ip"
done < <(arp -a)

# Procesar el archivo ethers_copy
while IFS= read -r ethers_line; do
    host=$(echo "$ethers_line" | awk '{print $1}')
    mac=$(echo "$ethers_line" | awk '{print $2}')
    
    if [[ "$host" == "$SEARCH_STRING"* ]]; then
        # Verificar si la MAC está en la tabla ARP
        if [ -n "${arp_table[$mac]}" ]; then
            # Si la MAC está en la tabla ARP, generar la entrada hostname-mac-ip-on
            echo "$host $mac ${arp_table[$mac]} on"
        else
            # Si la MAC no está en la tabla ARP, generar la entrada hostname-mac-none-off
            echo "$host $mac none off"
        fi
    fi
done < "$ETHER_FILE" > "$OUT_DIR/output_scan_$SEARCH_STRING.txt"
