import os
import subprocess
from flask import Flask, request, jsonify
from dotenv import load_dotenv

from database import iniciar_db, asignar_ip_dinamica

load_dotenv()
app = Flask(__name__)
conn = iniciar_db()

def configurar_red_sistema():
    try:
        subprocess.run(["wg", "show", "wg0"], check=True, stdout=subprocess.DEVNULL)
    except subprocess.CalledProcessError:
        subprocess.run(["wg-quick", "up", "wg0"], check=True)

def agregar_peer_wireguard(public_key, ip_virtual):
    subprocess.run([
        "wg", "set", "wg0",
        "peer", public_key,
        "allowed-ips", f"{ip_virtual}/32"
    ], check=True)

def guards(nombre, token, public_key):
    if not nombre or not public_key:
        return jsonify({"error": "missing fields"}), 400

    if len(nombre) > 64 or len(public_key) > 64:
        return jsonify({"error": "invalid input"}), 400

    if token != os.getenv("BOOTSTRAP_TOKEN"):
        return jsonify({"error": "unauthorized"}), 401
    
    return None

@app.route('/registrar', methods=['POST'])
def registrar_jetson():
    datos = request.json or {}

    nombre = datos.get('nombre')
    public_key = datos.get('public_key')
    token = datos.get('token')

    respuesta_guard = guards(nombre, token, public_key)
    if respuesta_guard:
        return respuesta_guard
    
    ip_asignada = asignar_ip_dinamica(conn, nombre, public_key)
    try:
        agregar_peer_wireguard(public_key, ip_asignada)
    except subprocess.CalledProcessError:
        return jsonify({"error": "wireguard failure"}), 500

    return jsonify({
        "ip_virtual": ip_asignada,
        "hub_public_key": os.getenv("HUB_PUBLIC_KEY"),
        "hub_endpoint": f"{os.getenv('HUB_ENDPOINT')}:{os.getenv('HUB_PORT', '51820')}"
    })


if __name__ == '__main__':
    configurar_red_sistema()
    app.run(host='10.0.0.1', port=5000)