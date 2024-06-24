#!/bin/bash

# Variables
playbook_file="run_test_file.yml"
inventory_file="/home/administrador/Documentos/Repositorios/tfg_app_web_proyecto/ansible/inventories/dynamic_inventory.ini"

# Crear el playbook de Ansible dinámicamente
cat <<EOF > $playbook_file
---
- name: Crear archivo de prueba en el escritorio
  hosts: online
  gather_facts: no  # No recopilar hechos sobre las máquinas remotas
  tasks:
    - name: Crear archivo de prueba en el escritorio
      ansible.builtin.file:
        path: "{{ lookup('env', 'HOME') }}/Escritorio/test_file.txt"
        state: touch
        mode: '0644'
        content: "This is a test for run_sh_files"
EOF

# Ejecutar el playbook de Ansible
ansible-playbook -i $inventory_file $playbook_file --ask-pass

# Limpiar archivos temporales
rm $playbook_file

