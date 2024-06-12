import subprocess
import os

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
VENV_PATH = "/home/administrador/Documentos/Repositorios/tfg_app_web_proyecto/venv"

def run_external_script(script_path):
    try:
        # Crea un script bash temporal para activar el entorno virtual y ejecutar el script Python
        bash_script = f"""
        #!/bin/bash
        source {VENV_PATH}/bin/activate
        python3.12 {script_path}
        """
        bash_script_path = os.path.join(CURRENT_DIR, 'run_script.sh')
        
        # Guarda el script bash en un archivo temporal
        with open(bash_script_path, 'w') as file:
            file.write(bash_script)
        
        # Asegúrate de que el script bash tenga permisos de ejecución
        os.chmod(bash_script_path, 0o755)

        # Ejecuta el script bash con sudo
        command = ['sudo', bash_script_path]

        # Ejecuta el script y captura la salida
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()

        # Elimina el script bash temporal
        os.remove(bash_script_path)

        # Verifica si la ejecución fue exitosa
        if process.returncode == 0:
            # Devuelve la salida decodificada del stdout
            return stdout.decode('utf-8')
        else:
            # Devuelve la salida de error decodificada en caso de error
            return stderr.decode('utf-8')
    except Exception as e:
        # Maneja excepciones y devuelve un mensaje de error
        return f"Error al ejecutar el script externo: {e}"
