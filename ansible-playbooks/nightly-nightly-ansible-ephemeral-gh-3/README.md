# Nightly Ansible Ephemeral GitHub Runner

Provision, health-check, and clean up ephemeral GitHub self-hosted runners on Linux hosts using Ansible.

## Features
- Provision runners with systemd service
- Health-check and auto-restart
- Clean up orphaned runners

## Quickstart
```bash
# Provision runners
ansible-playbook -i inventory.ini provision_runners.yml

# Health-check
ansible-playbook -i inventory.ini health_check.yml

# Cleanup
ansible-playbook -i inventory.ini cleanup_runners.yml
```

## License
MIT
