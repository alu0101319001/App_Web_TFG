# admin_web_app/views.py
import os
import subprocess
from datetime import datetime
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, JsonResponse
from django.views import View
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Computer
from .management.commands.execute_ansible_playbooks import execute_ansible_playbook
from .management.commands.execute_python_script import run_external_script
from .utils import run_scan_playbook, run_scan_update

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PLAYBOOKS_DIR = os.path.join(CURRENT_DIR, '../../ansible/playbooks')
INVENTORY_DIR = os.path.join(CURRENT_DIR, '../../ansible/inventories')
ANSIBLE_SCRIPTS_DIR = os.path.join(CURRENT_DIR, '../../ansible/scripts')

def is_admin(user):
    return user.is_superuser

@login_required
@user_passes_test(is_admin)
def base_page(request):
    # Obtener el timestamp actual
    timestamp = datetime.now().timestamp()

    context = {
        'timestamp': timestamp,
    }
    return render(request, 'base.html', context)

@login_required
@user_passes_test(is_admin)
def main_page(request):
    computers = Computer.objects.all()
    
    timestamp = datetime.now().timestamp()
    context = {
        'computers': computers,
        'timestamp': timestamp,
    }
    return render(request, 'main_page.html', context)

@login_required
@user_passes_test(is_admin)
def testing_page(request):
    computers = Computer.objects.all()
    
    timestamp = datetime.now().timestamp()
    context = {
        'computers': computers,
        'timestamp': timestamp,
    }
    return render(request, 'testing_page.html', context)

@login_required
@user_passes_test(is_admin)
def index(request):
    computers = Computer.objects.all()

    timestamp = datetime.now().timestamp()
    context = {
        'computers': computers,
        'timestamp': timestamp,
    }
    return render(request, 'computers/index.html', context)

@login_required
@user_passes_test(is_admin)
def get_computer_details(request, computer_id):
    computer = Computer.objects.get(pk=computer_id)
    data = {
        'name': computer.name,
        'state': computer.state,
        'mac': computer.mac,
        'ip': computer.ip,
        # Agregar más campos según sea necesario
    }
    return JsonResponse(data)

@login_required
@user_passes_test(is_admin)
def turn_on_all(request):
    print('turn_on_all')
    playbook_path = os.path.abspath(os.path.join(PLAYBOOKS_DIR, 'up_computers_down.yml'))
    print(playbook_path)
    print(PLAYBOOKS_DIR)
    inventory_path = os.path.abspath(os.path.join(INVENTORY_DIR, 'dynamic_inventory.ini'))
    output = execute_ansible_playbook(playbook_path, inventory_path)
    return HttpResponse(output)

@login_required
@user_passes_test(is_admin)
def turn_off_all(request):
    print('turn_off_all')
    playbook_path = os.path.abspath(os.path.join(PLAYBOOKS_DIR, 'down_computers_up.yml'))
    inventory_path = os.path.abspath(os.path.join(INVENTORY_DIR, 'dynamic_inventory.ini'))
    output = execute_ansible_playbook(playbook_path, inventory_path)
    return HttpResponse(output)

def run_scan(request):
    # Llama a las funciones para ejecutar los comandos
    playbook_result = run_scan_playbook()
    update_result = run_scan_update()
        
    # Devuelve los resultados como JSON al navegador
    return JsonResponse({
        'playbook_result': playbook_result,
        'update_result': update_result
    })

@login_required
@user_passes_test(is_admin)
def execute_playbook(request, playbook, hostname):
    playbook_path = os.path.abspath(os.path.join(PLAYBOOKS_DIR, playbook))
    inventory_path = os.path.abspath(os.path.join(INVENTORY_DIR, 'dynamic_inventory.ini'))
    extra_vars = f"target_host={hostname}"
    output = execute_ansible_playbook(playbook_path, inventory_path, extra_vars)
    return HttpResponse(output)

