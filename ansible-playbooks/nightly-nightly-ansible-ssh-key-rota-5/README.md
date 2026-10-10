# SSH Key Rotator Playbook

This playbook rotates SSH host keys on the target hosts. It backs up existing keys, generates new ones, and restarts the SSH service. Use with caution on production systems.

## Requirements

- Ansible 2.9+
- Sudo privileges on target hosts

## Usage

```sh
ansible-playbook -i inventory.ini src/rotate_ssh_keys.yml
```

## Inventory

Edit `inventory.ini` to list your hosts.
