# nightly-ansible-apt-mirror

## Summary
Sets up a local APT repository mirror and configures clients to use it, ensuring package availability even in the post‑apocalypse.

## Prerequisites
- Ansible 2.9+
- Ubuntu/Debian target
- Sufficient disk space for mirror

## Usage
```bash
ansible-playbook -i inventory.ini src/playbook.yml
```

## Variables
- `mirror_dir` (default: `/var/spool/apt-mirror`) – directory where the mirror is stored.
- `mirror_url` (default: `http://archive.ubuntu.com/ubuntu`) – upstream repository.
