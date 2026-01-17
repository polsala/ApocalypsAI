# nightly-ansible-apt-maintainer

Utility that runs an Ansible playbook to clean up apt packages on Debian/Ubuntu systems. It updates the package cache, removes unused packages, cleans the local repository, and reports the actions taken.

## Usage

```sh
ansible-playbook -i src/inventory.ini src/playbook.yml
```

The playbook is safe to run in check mode (`--check`) to preview changes.

## Files

- `src/playbook.yml` – The Ansible playbook.
- `src/inventory.ini` – Inventory targeting localhost.
- `tests/test_playbook.py` – Simple tests ensuring the playbook contains expected tasks.
