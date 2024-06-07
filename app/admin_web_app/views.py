# admin_web_app/views.py
import os
from datetime import datetime
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, JsonResponse
from .models import Computer
from .management.commands.execute_ansible_playbooks import execute_ansible_playbook
from .management.commands.execute_python_script import run_external_script

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PLAYBOOKS_DIR = os.path.join(CURRENT_DIR, '../../ansible/playbooks')
INVENTORY_DIR = os.path.join(CURRENT_DIR, '../../ansible/inventories')
ANSIBLE_SCRIPTS_DIR = os.path.join(CURRENT_DIR, '../../ansible/scripts')

def base_page(request):
    # Obtener el timestamp actual
    timestamp = datetime.now().timestamp()

    context = {
        'timestamp': timestamp,
    }
    return render(request, 'base.html', context)

def main_page(request):
    computers = Computer.objects.all()
    
    timestamp = datetime.now().timestamp()
    context = {
        'computers': computers,
        'timestamp': timestamp,
    }
    return render(request, 'main_page.html', context)

def testing_page(request):
    computers = Computer.objects.all()
    
    timestamp = datetime.now().timestamp()
    context = {
        'computers': computers,
        'timestamp': timestamp,
    }
    return render(request, 'testing_page.html', context)

def index(request):
    computers = Computer.objects.all()

    timestamp = datetime.now().timestamp()
    context = {
        'computers': computers,
        'timestamp': timestamp,
    }
    return render(request, 'computers/index.html', context)

def computer_detail(request, computer_id):
    computers = get_object_or_404(Computer, id=computer_id)

    timestamp = datetime.now().timestamp()
    context = {
        'computers': computers,
        'timestamp': timestamp,
    }
    return render(request, 'computers/computer_detail.html', context)

def turn_on_all(request):
    print('turn_on')
    playbook_path = os.path.join(PLAYBOOKS_DIR, 'up_computers_down.yml')
    print(playbook_path)
    print(PLAYBOOKS_DIR)
    inventory_path = os.path.join(INVENTORY_DIR, 'dynamic_inventory.ini')
    output = execute_ansible_playbook(playbook_path, inventory_path)
    return HttpResponse(output)

def turn_off_all(request):
    print('turn_off')
    playbook_path = os.path.join(PLAYBOOKS_DIR, 'down_computers_up.yml')
    inventory_path = os.path.join(INVENTORY_DIR, 'dynamic_inventory.ini')
    output = execute_ansible_playbook(playbook_path, inventory_path)
    return HttpResponse(output)

def update_view(request):
    # Obtén la ruta absoluta del script
    script_path = os.path.abspath(os.path.join(ANSIBLE_SCRIPTS_DIR, 'run_scan_workflow.py'))
    # Ejecuta el script externo y captura la salida
    output = run_external_script(script_path)
    return HttpResponse(output)
