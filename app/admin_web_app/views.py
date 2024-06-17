# admin_web_app/views.py
import os
import json
import subprocess
from datetime import datetime
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, JsonResponse
from django.views import View
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from .models import Computer
from .management.commands.execute_ansible_playbooks import execute_ansible_playbook
from .management.commands.execute_python_script import run_external_script
from .utils import run_scan_playbook, run_scan_update, run_copyFiles_playbook

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PLAYBOOKS_DIR = os.path.join(CURRENT_DIR, '../../ansible/playbooks')
INVENTORY_DIR = os.path.join(CURRENT_DIR, '../../ansible/inventories')
ANSIBLE_SCRIPTS_DIR = os.path.join(CURRENT_DIR, '../../ansible/scripts')
STATIC_DIR = os.path.join(CURRENT_DIR, 'static')

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
        'id': computer.id,  # Añade el campo id
        'name': computer.name,
        'state': computer.state,
        'mac': computer.mac,
        'ip': computer.ip,
        'warning': computer.warning,
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
        'update_result': [update_result]
    })

@login_required
@user_passes_test(is_admin)
def execute_playbook(request, playbook, hostname):
    playbook_path = os.path.abspath(os.path.join(PLAYBOOKS_DIR, playbook))
    inventory_path = os.path.abspath(os.path.join(INVENTORY_DIR, 'dynamic_inventory.ini'))
    extra_vars = f"target_host={hostname}"
    output = execute_ansible_playbook(playbook_path, inventory_path, extra_vars)
    return HttpResponse(output)


@csrf_exempt
@login_required
@user_passes_test(is_admin)
def run_sh_script(request):
    if request.method == 'POST' and request.FILES.get('scriptFile'):
        script_file = request.FILES['scriptFile']
        script_path = os.path.abspath(os.path.join(STATIC_DIR, 'bash'))
        argument = request.POST.get('argument', '').strip()  # Obtener el argumento del POST (opcional)

        try:
            # Guardar el archivo en el directorio de scripts
            with open(script_path + script_file.name, 'wb+') as destination:
                for chunk in script_file.chunks():
                    destination.write(chunk)

            # Ejecutar el script de bash con el argumento (si está presente)
            if argument:
                result = subprocess.run(['bash', script_path + script_file.name, argument],
                                        capture_output=True, text=True)
            else:
                result = subprocess.run(['bash', script_path + script_file.name],
                                        capture_output=True, text=True)

            output = result.stdout

            return JsonResponse({'output': output})

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Invalid request method'}, status=400)

@csrf_exempt
def copy_files(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        folder = data.get('folder')
        files = data.get('files')

        if folder and files:
            # Llamar a la función que ejecuta el playbook de Ansible
            result = run_copyFiles_playbook(folder, files)

            if isinstance(result, dict) and 'summary_message' in result:
                summary_message = result['summary_message']
                return JsonResponse({'summary_message': summary_message})
            else:
                error_message = "Unexpected or missing result from playbook execution."
                return JsonResponse({'message': error_message}, status=500)

    return JsonResponse({'message': 'Invalid request'}, status=400)

@csrf_exempt
def execute_command(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        command = data.get('command')
        hostname = data.get('hostname')
        target_host = hostname if hostname else "online"

        playbook_path = os.path.join(settings.PROJECT_PATH, 'ansible', 'playbooks', 'execute_command.yml')
        inventory_path = os.path.join(settings.PROJECT_PATH, 'ansible', 'inventories', 'dynamic_inventory.ini')

        command = [
            'ansible-playbook',
            playbook_path,
            '-i', inventory_path,
            '--extra-vars', f'command={command} target_host={target_host}'
        ]

        try:
            result = subprocess.run(command, capture_output=True, text=True, check=True)
            return JsonResponse({'message': result.stdout})
        except subprocess.CalledProcessError as e:
            return JsonResponse({'error': f'Error executing playbook: {e.stderr}'}, status=500)

    return JsonResponse({'error': 'Invalid request'}, status=400)

@login_required
@user_passes_test(is_admin)
@csrf_exempt
def toggle_warning(request, computer_id):
    computer = Computer.objects.get(pk=computer_id)
    if request.method == 'POST':
        computer.warning = not computer.warning
        if computer.warning == True:
            computer.icon = 'computer--exclamation.png'
        else:
            computer.icon = 'computer-off.png'
        computer.save()
        return JsonResponse({'success': True, 'warning': computer.warning})
    return JsonResponse({'error': 'Invalid request method'}, status=400)

