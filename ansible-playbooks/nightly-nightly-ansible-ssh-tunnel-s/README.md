# Nightly Ansible SSH Tunnel Setup

## Overview
This playbook creates a systemd service that maintains a reverse SSH tunnel from the target host back to a central server, enabling remote access to machines behind NAT or firewalls.

## Requirements
- Ansible 2.9+
- SSH key pair pre‑shared between target and central server
- sudo privileges on target

## Usage
```bash
ansible-playbook -i inventory.ini src/setup_tunnel.yml -e "remote_user=ubuntu tunnel_user=ssh_tunnel remote_host=central.example.com remote_port=2222"
```

## Variables
- `tunnel_user` (default: `ssh_tunnel`) – user under which the service runs.
- `remote_user` – user on the central server to connect as.
- `remote_host` – hostname or IP of the central server.
- `remote_port` (default: `2222`) – port on the central server to forward to.
- `local_port` (default: `22`) – local port to expose.

## How it works
The playbook creates a systemd unit file `/etc/systemd/system/ssh-reverse-tunnel.service` that runs `ssh -N -R ${remote_port}:localhost:${local_port} ${remote_user}@${remote_host}` (via `autossh` for resilience) and ensures the service is enabled and started.

## License
MIT
