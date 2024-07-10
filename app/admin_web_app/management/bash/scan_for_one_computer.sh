#!/bin/bash

# Verificar si se proporciona el argumento de hostname
if [ $# -ne 1 ]; then
    echo "Uso: $0 <nombre_host>"
    exit 1
fi

# Establecer rutas y nombres de archivos
PROJECT_DIR="$HOME/Documentos/Repositorios/tfg_app_web_proyecto"
ETHER_FILE="$PROJECT_DIR/registers/ethers_copy"
OUT_DIR="$PROJECT_DIR/outputs/scan_for_hosts/"

# Nombre del host objetivo
TARGET_HOST="$1"

# Imprimir mensaje de depuración
echo "Host objetivo: $TARGET_HOST"

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
    ping -c 1 -W 1 "$ip" >/dev/null 2>&1
    return $?
}

# Procesar el archivo ethers_copy para el host específico
while IFS= read -r ethers_line; do
    host=$(echo "$ethers_line" | awk '{print $1}')
    mac=$(echo "$ethers_line" | awk '{print $2}')
    
    if [[ "$host" == "$TARGET_HOST" ]]; then
        if [ -n "${arp_table[$mac]}" ]; then
            ip="${arp_table[$mac]}"
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
done < "$ETHER_FILE" > "$OUT_DIR/output_scan_$TARGET_HOST.txt"

# Esperar a que finalicen todos los procesos en segundo plano
wait
