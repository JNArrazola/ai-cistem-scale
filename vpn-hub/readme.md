```bash
sudo ufw allow 51820/udp
```
---
```bash
sudo pacman -S wireguard-tools
sudo pacman -S linux-headers wireguard-dkms

```
---
```bash
cd /etc/wireguard
sudo wg genkey | sudo tee hub_private.key | sudo wg pubkey | sudo tee hub_public.key
```
---
```bash
sudo nano /etc/wireguard/wg0.conf
```
---
```bash
[Interface]
Address = 10.0.0.1/24
ListenPort = 51820
PrivateKey = <CONTENIDO DE hub_private.key>
SaveConfig = false
```
---
```bash
sudo chmod 600 /etc/wireguard/wg0.conf
```
---
```bash
sudo wg-quick up wg0
```