#!/bin/bash

# Actualizar los paquetes del sistema
sudo apt update
# Instalar git
sudo apt install -y git
# Entrar al directorio del proyecto
cd proyecto_tfg_admin
# Instalar Python y pip
sudo apt install -y python3 python3-pip
# Instalar Ansible
sudo apt install -y ansible

# Crear y activar un entorno virtual para el proyecto Django
python3 -m venv venv
source venv/bin/activate

# Instalar Django y otras dependencias del proyecto Django
pip install -r requirements.txt

# Mostrar mensaje de finalización
echo "Instalación completada. Ahora puedes empezar a trabajar en tu proyecto Django y Ansible."
