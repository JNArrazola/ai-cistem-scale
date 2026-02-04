import os
from dotenv import load_dotenv

from wireguard import generar_claves, escribir_config, levantar_tunel
from bootstrap import registrar_en_hub
from functions import heartbeat

import time

load_dotenv()

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

    while True:
        heartbeat(hub_url, nombre)
        print(f"Heartbeat enviado desde '{nombre}' al hub '{hub_url}'")
        time.sleep(int(os.getenv("HEARTBEAT_INTERVAL", 30)))

if __name__ == "__main__":
    main()
