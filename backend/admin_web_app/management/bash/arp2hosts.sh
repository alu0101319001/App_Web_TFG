#!/bin/bash

## 1 - Define algunas variables de archivo y directorio
FICH_ARP=/run/user/arp$$.log
FICH_HOST=/etc/hosts
FICH_HOST_CAB=/etc/hosts_cabecera
ETHERS_FILE=/root/bin/ethers

## Crear el directorio logs si no existe
LOG_DIR=$(pwd)/logs
mkdir -p $LOG_DIR

## Definir archivo de log en el directorio logs
LOG_FILE=$LOG_DIR/hosts_output_$(date -Iseconds).log


## 2 - Ejectua un escaneo de red usando Nmap
#nmap -sP -PR -n -oG - 10.213.30.0/24 &>/dev/null
#arp -n > $FICH_ARP
nmap -sP -PR -n -oN - 10.209.2.0/24 \
  | awk 'BEGIN {RS="\nNmap"; FS="\n"} {print $1,tolower($3)}' > $FICH_ARP

mv $FICH_HOST ${FICH_HOST}.old
cp $FICH_HOST_CAB $FICH_HOST

echo "# actualizado en $(date -Iseconds)"  >> $FICH_HOST
cat $ETHERS_FILE | cut -f2 | while read ma
do 
  maMac=$(grep $ma $ETHERS_FILE | cut -f1)
  ip=$(cat $FICH_ARP | grep $maMac | cut -f5 -d' ')
  if [ ! -z "$ip" ]
  then
    echo -e "$ip\t${ma}.isaatc.ull.es\t${ma}\t# $maMac" >> $FICH_HOST
  fi
done

## Guardar la salida procesada en el archivo de log
cp $FICH_HOST $LOG_FILE

#rm $FICH_ARP