import configparser
import sys

def obtener_macs(ruta_archivo, script_function, nombre_host=None):
    config = configparser.ConfigParser()
    config.read(ruta_archivo)

    macs = []

    if script_function == "offline":
        section = "offline"
    elif script_function == "online":
        section = "online"
    elif script_function == "warning":
        section = "warning"
    elif script_function == "examMode":
        section = "examMode"
    else:
        print("Error: El argumento script_function debe ser 'offline','online','warning' o 'examMode'.")
        sys.exit(1)

    if section in config:
        if nombre_host:
            for key, value in config[section].items():
                if key.startswith(nombre_host):
                    values = value.split()
                    for v in values:
                        if v.startswith('mac_address='):
                            mac_address = v.split('=')[1]
                            if mac_address != 'none':
                                macs.append(mac_address)
                                break
        else:
            for key, value in config[section].items():
                # Dividir el valor en sus partes correspondientes
                values = value.split()
                # Buscar la clave 'mac_address' en las partes divididas
                for v in values:
                    if v.startswith('mac_address='):
                        mac_address = v.split('=')[1]
                        if mac_address != 'none':
                            macs.append(mac_address)
                            break

    return macs

if __name__ == "__main__":
    if len(sys.argv) not in [3, 4]:
        print("Uso: python3.12 script.py <ruta_archivo_ini> <script_function> [nombre_host]")
        sys.exit(1)

    ruta_archivo_ini = sys.argv[1]
    script_function = sys.argv[2]

    # Obtener el nombre del host si se proporciona como argumento
    nombre_host = sys.argv[3] if len(sys.argv) == 4 else None

    macs = obtener_macs(ruta_archivo_ini, script_function, nombre_host)
    print(macs)
