import os
import platform
from dotenv import load_dotenv

load_dotenv()

COMMANDS = {
    "ubuntu": {
            "install": "sudo apt install -y wireguard",
            "service": "wg-quick",
            "config_path": "/etc/wireguard/"
        },
    "arch": {
        "install": "sudo pacman -S --noconfirm wireguard-tools",
        "service": "wg-quick",
        "config_path": "/etc/wireguard/"
    }
}

def get_command(distro, command):
    distro_commands = COMMANDS.get(distro)
    if distro_commands:
        return distro_commands.get(command)
    return None

def get_distro():
    return os.getenv("SO_TYPE", platform.linux_distribution()[0].lower() if hasattr(platform, 'linux_distribution') else "ubuntu")