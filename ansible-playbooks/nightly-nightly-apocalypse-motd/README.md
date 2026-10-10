# Apocalypse MOTD

A whimsical Ansible playbook that installs a rotating "Apocalypse of the Day" message of the day (MOTD) with random post‑apocalyptic quotes. Useful for adding a bit of flavor to servers.

## Usage

```bash
ansible-playbook -i src/inventory.ini src/playbook.yml -e "motd_path=/etc/motd"
```

To test locally without sudo, specify a writable path:

```bash
ansible-playbook -i src/inventory.ini src/playbook.yml -e "motd_path=./test_motd.txt"
```

The playbook installs a template that selects a random quote from a predefined list.

## Files

- `src/playbook.yml` – entry point.
- `src/roles/apocalypse_motd/` – role with tasks, vars, and template.
- `tests/run_test.sh` – simple CI test.
