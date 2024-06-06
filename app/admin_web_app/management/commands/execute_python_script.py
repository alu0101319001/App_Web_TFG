import subprocess
from django.http import HttpResponse

def run_external_script(request, script_path):
    try:
        # Ejecuta el script externo
        subprocess.run(['python3.12', script_path])
        return HttpResponse("Script externo ejecutado correctamente")
    except Exception as e:
        return HttpResponse(f"Error al ejecutar el script externo: {e}")
