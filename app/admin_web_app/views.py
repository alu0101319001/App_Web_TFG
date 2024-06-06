# admin_web_app/views.py
import os
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Computer
from .management.commands.execute_ansible_playbooks import execute_ansible_playbook

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PLAYBOOKS_DIR = os.path.join(CURRENT_DIR, '../../ansible/playbooks')
INVENTORY_DIR = os.path.join(CURRENT_DIR, '../../ansible/inventories')

def base_page(request):
    return render(request, 'base.html')

def main_page(request):
    computers = Computer.objects.all()
    return render(request, 'main_page.html', {'computers': computers})

def testing_page(request):
    computers = Computer.objects.all()
    return render(request, 'testing_page.html', {'ordenadores': computers})

def index(request):
    computers = Computer.objects.all()
    return render(request, 'computers/index.html', {'computers': computers})

def computer_detail(request, computer_id):
    computer = get_object_or_404(Computer, id=computer_id)
    return render(request, 'computers/computer_detail.html', {'computer': computer})

def turn_on_all(request):
    playbook_path = os.path.join(PLAYBOOKS_DIR, '/up_computers_down.yml')
    inventory_path = os.path.join(INVENTORY_DIR, '/dynamic_inventory.ini')
    execute_ansible_playbook(playbook_path, inventory_path)
    return HttpResponse("Playbook para encender todos los dispositivos ejecutado correctamente.")

def turn_off_all(request):
    playbook_path = os.path.join(PLAYBOOKS_DIR, '/down_computers_up.yml')
    inventory_path = os.path.join(INVENTORY_DIR, '/dynamic_inventory.ini')
    execute_ansible_playbook(playbook_path, inventory_path)
    return HttpResponse("Playbook para apagar todos los dispositivos ejecutado correctamente.")

def update_view(request):
    return HttpResponse("Playbook para apagar todos los dispositivos ejecutado correctamente.")
