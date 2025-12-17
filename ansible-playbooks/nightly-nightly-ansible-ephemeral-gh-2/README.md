# Nightly Ansible Ephemeral GitHub Runner

Provision, configure, and tear down ephemeral self-hosted GitHub Actions runners on target hosts using Ansible. Includes health checks, graceful shutdown, and cleanup.

## Features
- Idempotent provisioning of runners
- Health check and status reporting
- Graceful shutdown and cleanup
- Configurable runner labels and token
- Works with Linux hosts (systemd)

## Requirements
- Ansible 2.14+
- Python 3.11+ on controller
- Target host with systemd and Docker (optional)
- GitHub PAT or runner registration token

## Usage
```bash
ansible-playbook -i inventory.ini provision_runners.yml
ansible-playbook -i inventory.ini health_check.yml
ansible-playbook -i inventory.ini cleanup_runners.yml
```

## Variables
See `vars/main.yml` for defaults and override via inventory or extra vars.

## License
MIT
