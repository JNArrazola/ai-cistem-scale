import os
import subprocess

KEY_DIR = "keys"

def generar_claves():
    os.makedirs(KEY_DIR, exist_ok=True)

    private_key = f"{KEY_DIR}/private.key"
    public_key = f"{KEY_DIR}/public.key"

    if not os.path.exists(private_key):
        subprocess.run(
            f"wg genkey | tee {private_key} | wg pubkey > {public_key}",
            shell=True,
            check=True
        )

    return private_key, public_key

def escribir_config(data, private_key_path):
    with open(private_key_path) as f:
        private_key = f.read().strip()

    config = f"""
[Interface]
PrivateKey = {private_key}
Address = {data['ip_virtual']}/24
DNS = 10.0.0.1

[Peer]
PublicKey = {data['hub_public_key']}
Endpoint = {data['hub_endpoint']}
AllowedIPs = 10.0.0.0/0
PersistentKeepalive = 25
"""

    os.chmod("/etc/wireguard", 0o600)
    with open("/etc/wireguard/wg0.conf", "w") as f:
        f.write(config)

def levantar_tunel():
    try:
        subprocess.run(["wg", "show", "wg0"], check=True, stdout=subprocess.DEVNULL)
    except subprocess.CalledProcessError:
        subprocess.run(["wg-quick", "up", "wg0"], check=True)
