# nightly-ansible-apt-mirror-sync

Utility to set up an apt-mirror on a host and optionally sync it to other hosts, enabling offline package installation in a post‑apocalyptic environment.

## Usage

```bash
ansible-playbook -i inventory.ini src/playbook.yml
```

## Variables

- `mirror_url`: URL of the upstream mirror (default: `http://archive.ubuntu.com/ubuntu`)
- `target_dir`: directory where the mirror is stored (default: `/var/spool/apt-mirror`)

## Inventory

Create an `inventory.ini` file (see `src/inventory.ini`) with a `[mirror]` group for the host that will host the mirror and an optional `[clients]` group for hosts that should receive a synced copy.

## License

MIT
