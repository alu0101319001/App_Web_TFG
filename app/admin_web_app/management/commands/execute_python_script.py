import subprocess

def run_external_script(script_path):
    try:
        # Construye el comando para ejecutar el script externo
        command = ['sudo', 'python3.12', script_path]

        # Ejecuta el script externo y captura la salida
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()

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
