import os
from dotenv import load_dotenv

from wireguard import generar_claves, escribir_config, levantar_tunel
from bootstrap import registrar_en_hub

load_dotenv()

def main():
    nombre = os.getenv("NODE_NAME")
    hub_url = os.getenv("HUB_URL")
    token = os.getenv("BOOTSTRAP_TOKEN")

    private_key, public_key = generar_claves()
    data = registrar_en_hub(hub_url, nombre, public_key, token)
    escribir_config(data, private_key)
    levantar_tunel()

if __name__ == "__main__":
    main()
