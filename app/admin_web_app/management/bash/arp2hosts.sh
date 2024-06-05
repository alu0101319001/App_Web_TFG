#!/bin/bash

## 1 - Define algunas variables de archivo y directorio
FICH_ARP=/run/user/arp$$.log
FICH_HOST=/etc/hosts
FICH_HOST_CAB=/etc/hosts_cabecera
ETHERS_FILE=/root/bin/ethers

## Crear el directorio logs si no existe
LOG_DIR=../../../../logs
mkdir -p $LOG_DIR

## Definir archivo de log en el directorio logs
LOG_FILE=$LOG_DIR/hosts_copy.log

## 2 - Ejecuta un escaneo de red usando Nmap
sudo nmap -sP -PR -n -oN - 10.209.2.0/24 \
  | awk 'BEGIN {RS="\nNmap"; FS="\n"} {print $1,tolower($3)}' > $FICH_ARP

## Mover el archivo de hosts actual a una copia de respaldo
mv $FICH_HOST ${FICH_HOST}.old
## Copiar la cabecera del archivo de hosts
cp $FICH_HOST_CAB $FICH_HOST

sudo echo "# actualizado en $(date -Iseconds)"  >> $FICH_HOST
sudo cat $ETHERS_FILE | while read line
do 
  host=$(echo "$line" | cut -f1)
  ma=$(echo "$line" | cut -f2)
  ip=$(grep $ma $FICH_ARP | cut -f5 -d' ')
  if [ ! -z "$ip" ]
  then
    sudo echo -e "$ip\t${host}.isaatc.ull.es\t${host}\t# $ma" >> $FICH_HOST
  fi
done

## Guardar la salida procesada en el archivo de log
sudo cp $FICH_HOST $LOG_FILE

#rm $FICH_ARP
