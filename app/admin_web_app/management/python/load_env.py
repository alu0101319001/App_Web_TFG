import os

BASE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../../../')

def load_env_variables(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    # Sustituir la etiqueta $BASE con la ruta base del proyecto
    modified_lines = [line.replace('$BASE', BASE_DIR) for line in lines]

    # Parsear las variables y establecerlas como variables de entorno
    for line in modified_lines:
        key, value = line.strip().split('=')
        os.environ[key] = value

