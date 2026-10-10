# Nightly Apt Upgrade Scheduler

## Overview
This Ansible playbook configures a nightly `apt` upgrade on Debian/Ubuntu systems and sprinkles a random motivational quote onto `/etc/motd` after each upgrade. It ensures the `unattended-upgrades` package is present, creates a cron job that runs at 02:00 AM, and updates the MOTD with a whimsical line.

## Requirements
- Ansible 2.9+ installed on the control machine
- Sudo/root privileges on the target host (the playbook uses `become: true`)
- Target hosts must be Debian‑based (apt package manager)

## Usage
```bash
# From the repository root
ansible-playbook -i ansible-playbooks/nightly-ansible-apt-upgrade-scheduler/src/inventory.ini \
               ansible-playbooks/nightly-ansible-apt-upgrade-scheduler/src/apt_upgrade.yml
```

## Files
- `src/apt_upgrade.yml` – The main playbook
- `src/inventory.ini` – Simple inventory targeting the local machine
- `tests/test_apt_upgrade.yml` – Automated test that validates the playbook syntax

## License
MIT – see the repository LICENSE file.
