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

# Función para comprobar si la máquina está encendida
function check_ping {
    local ip="$1"
    ping -c 1 -W 1 "$ip" >/dev/null 2>&1  # Espera 1 segundo (-W 1) y realiza solo un intento de ping (-c 1)
    return $?
}

# Procesar el archivo ethers_copy en paralelo
while IFS= read -r ethers_line; do
    host=$(echo "$ethers_line" | awk '{print $1}')
    mac=$(echo "$ethers_line" | awk '{print $2}')
    
    if [[ "$host" == "$SEARCH_STRING"* ]]; then
        # Verificar si la MAC está en la tabla ARP
        if [ -n "${arp_table[$mac]}" ]; then
            ip="${arp_table[$mac]}"
            # Comprobar si la máquina responde al ping en paralelo
            {
                if check_ping "$ip"; then
                    echo "$host $mac $ip on"
                else
                    echo "$host $mac $ip off"
                fi
            } &
        else
            echo "$host $mac none off"
        fi
    fi
done < "$ETHER_FILE" > "$OUT_DIR/output_scan_$SEARCH_STRING.txt"

# Esperar a que finalicen todos los procesos en segundo plano
wait
