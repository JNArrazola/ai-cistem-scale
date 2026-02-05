import os
from dotenv import load_dotenv

from wireguard import generar_claves, escribir_config, levantar_tunel, generar_nuevas_claves, solicitar_rotacion, aplicar_nueva_clave
from bootstrap import registrar_en_hub
from functions import heartbeat
import threading

ROTATE_INTERVAL = int(os.getenv("ROTATE_INTERVAL", 86400))
HEARTHBEAT_INTERVAL = int(os.getenv("HEARTBEAT_INTERVAL", 30))

import time

load_dotenv()

def heartbeat_loop(hub_url, nombre):
    while True:
        heartbeat(hub_url, nombre)
        time.sleep(HEARTHBEAT_INTERVAL)

def rotation_loop(hub_url, nombre, token):
    while True:
        time.sleep(ROTATE_INTERVAL)
        print(f"Iniciando rotación de claves para el nodo '{nombre}'")
        generar_nuevas_claves()
        solicitar_rotacion(hub_url, nombre, token)
        aplicar_nueva_clave()
        print(f"Rotación de claves realizada para el nodo '{nombre}'")

def main():
    nombre = os.getenv("NODE_NAME")
    hub_url = os.getenv("HUB_URL")
    token = os.getenv("BOOTSTRAP_TOKEN")

    print(f"Registrando nodo '{nombre}' en el hub '{hub_url}' con token '{token}'")

    private_key, public_key = generar_claves()

    print(f"Claves generadas para el nodo '{nombre}':")
    print(f"  - Private Key: {private_key}")
    print(f"  - Public Key: {public_key}")

    data = registrar_en_hub(hub_url, nombre, public_key, token)
    escribir_config(data, private_key)
    levantar_tunel()

    heartbeat_thread = threading.Thread(target=heartbeat_loop, args=(hub_url, nombre), daemon=True).start()
    rotation_thread = threading.Thread(target=rotation_loop, args=(hub_url, nombre, token), daemon=True).start()

    while True:
        time.sleep(3600)

if __name__ == "__main__":
    main()
