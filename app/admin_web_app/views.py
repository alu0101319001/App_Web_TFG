# admin_web_app/views.py
import os
import json
import subprocess
import logging
from datetime import datetime
from functools import wraps
from django.urls import reverse
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.views import View
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import Group
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from .models import Computer
from .management.commands.execute_ansible_playbooks import execute_ansible_playbook
from .management.commands.execute_python_script import run_external_script
from .utils import run_scan_playbook, run_scan_update, run_copyFiles_playbook

logger = logging.getLogger(__name__)

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PLAYBOOKS_DIR = os.path.join(CURRENT_DIR, '../../ansible/playbooks')
INVENTORY_DIR = os.path.join(CURRENT_DIR, '../../ansible/inventories')
ANSIBLE_SCRIPTS_DIR = os.path.join(CURRENT_DIR, '../../ansible/scripts')
STATIC_DIR = os.path.join(CURRENT_DIR, 'static')

def is_admin(user):
    return user.is_superuser

def in_groups(user, group_names):
    return user.groups.filter(name__in=group_names).exists()

def group_required(group_names):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if in_groups(request.user, group_names):
                return view_func(request, *args, **kwargs)
            else:
                messages.error(request, "No tienes los permisos necesarios para acceder a esta página.")
                return redirect('access_denied')
        return _wrapped_view
    return decorator

def access_denied(request):
    return render(request, 'access_denied.html')

@login_required
@group_required(['profesorado', 'admin_group'])
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
@group_required(['profesorado', 'admin_group', 'alumnado'])
def index(request):
    computers = Computer.objects.all()

    timestamp = datetime.now().timestamp()
    context = {
        'computers': computers,
        'timestamp': timestamp,
    }
    return render(request, 'computers/index.html', context)

@login_required
@group_required(['profesorado', 'admin_group'])
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
@group_required(['profesorado', 'admin_group'])
def turn_on_all(request):
    print('turn_on_all')
    playbook_path = os.path.abspath(os.path.join(PLAYBOOKS_DIR, 'up_computers_down.yml'))
    print(playbook_path)
    print(PLAYBOOKS_DIR)
    inventory_path = os.path.abspath(os.path.join(INVENTORY_DIR, 'dynamic_inventory.ini'))
    output = execute_ansible_playbook(playbook_path, inventory_path)
    return HttpResponse(output)

@login_required
@group_required(['profesorado', 'admin_group'])
def turn_off_all(request):
    print('turn_off_all')
    playbook_path = os.path.abspath(os.path.join(PLAYBOOKS_DIR, 'down_computers_up.yml'))
    inventory_path = os.path.abspath(os.path.join(INVENTORY_DIR, 'dynamic_inventory.ini'))
    output = execute_ansible_playbook(playbook_path, inventory_path)
    return HttpResponse(output)

@group_required(['profesorado', 'admin_group'])
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
@group_required(['profesorado', 'admin_group'])
def execute_playbook(request, playbook, hostname):
    playbook_path = os.path.abspath(os.path.join(PLAYBOOKS_DIR, playbook))
    inventory_path = os.path.abspath(os.path.join(INVENTORY_DIR, 'dynamic_inventory.ini'))
    extra_vars = f"target_host={hostname}"

    if request.method == 'POST':
        try:
            # Parse the JSON body
            body = json.loads(request.body)
            custom_command = body.get('custom_command')
            
            # If a custom command is provided, add it to the extra_vars
            if custom_command:
                extra_vars += f" custom_command='{custom_command}'"
            
            output = execute_ansible_playbook(playbook_path, inventory_path, extra_vars)
            return JsonResponse({'output': output})
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    
    elif request.method == 'GET':
        output = execute_ansible_playbook(playbook_path, inventory_path, extra_vars)
        return HttpResponse(output, content_type='text/plain')
    
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)



@csrf_exempt
@login_required
@group_required(['profesorado', 'admin_group'])
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
@group_required(['profesorado', 'admin_group', 'alumnado'])
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
@group_required(['profesorado', 'admin_group'])
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
@csrf_exempt
@group_required(['profesorado', 'admin_group'])
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

@csrf_exempt
@group_required(['profesorado', 'admin_group'])
def sync_list(request):
    if request.method == 'POST':
        sync_file = request.FILES.get('sync_file')
        target_directory = request.POST.get('target_directory')

        if not sync_file:
            return JsonResponse({'error': 'Sync file not provided'}, status=400)
        if not target_directory:
            return JsonResponse({'error': 'Target directory not provided'}, status=400)

        # Guardar el archivo en el sistema de archivos del servidor
        fs = FileSystemStorage()
        filename = fs.save(sync_file.name, sync_file)
        uploaded_file_path = fs.path(filename)

        # Ejecutar el playbook de Ansible
        playbook_path = os.path.join(settings.PROJECT_PATH, 'ansible', 'playbooks', 'sync_list.yml')
        inventory_path = os.path.join(settings.PROJECT_PATH, 'ansible', 'inventories', 'dynamic_inventory.ini')
        command = [
            'ansible-playbook',
            playbook_path,
            '-i', inventory_path,
            '--extra-vars',
            f"lst_file={uploaded_file_path} target_directory={target_directory}"
        ]
        try:
            result = subprocess.run(command, capture_output=True, text=True, check=True)
            if result.returncode != 0:
                return JsonResponse({'error': result.stderr}, status=500)

            return JsonResponse({'message': 'Sync started successfully'})

        except subprocess.CalledProcessError as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Invalid request'}, status=400)

@require_http_methods(["POST"])
def activate_exam_mode(request, hostname='all'):
    playbook_path = os.path.join(settings.PROJECT_PATH, 'ansible', 'playbooks', 'change_to_exm.yml')
    inventory_path = os.path.join(settings.PROJECT_PATH, 'ansible', 'inventories', 'dynamic_inventory.ini')
    extra_vars = f"target_host={hostname}" if hostname != 'all' else None

    output = execute_ansible_playbook(playbook_path, inventory_path, extra_vars)
    return JsonResponse({'status': 0 if 'Error' not in output else 1, 'output': output})

@require_http_methods(["POST"])
def deactivate_exam_mode(request, hostname='all'):
    playbook_path = os.path.join(settings.PROJECT_PATH, 'ansible', 'playbooks', 'change_to_normal.yml')
    inventory_path = os.path.join(settings.PROJECT_PATH, 'ansible', 'inventories', 'dynamic_inventory.ini')
    extra_vars = f"target_host={hostname}" if hostname != 'all' else None

    output = execute_ansible_playbook(playbook_path, inventory_path, extra_vars)
    return JsonResponse({'status': 0 if 'Error' not in output else 1, 'output': output})


