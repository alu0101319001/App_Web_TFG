#!/bin/bash

# Obtener la tabla ARP
arp -a | while read -r line
do
    # Extraer la IP de cada línea de la salida de arp
    ip=$(echo $line | awk '{print $2}' | tr -d '()')
    
    # Resolver el nombre de host
    hostname=$(nslookup $ip | awk -F 'name = ' '/name = / { print $2 }' | tr -d '.')
    
    # Imprimir IP, MAC y nombre de host en una línea
    echo "$hostname $line"
done | sort
