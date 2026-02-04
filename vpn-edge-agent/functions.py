def heartbeat(hub_url, nombre):
    requests.post(
        f"{hub_url}/heartbeat",
        json={"nombre": nombre},
        timeout=5
    )
