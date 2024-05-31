#!/bin/bash

# Actualizar los paquetes del sistema
sudo apt update

# Instalar git
sudo apt install -y git

# Clonar el repositorio
git config user.name "alu0101319001"
git config user.email alu0101319001@ull.edu.es
git clone https://github.com/alu0101319001/App_Web_TFG.git proyecto_tfg_admin

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
