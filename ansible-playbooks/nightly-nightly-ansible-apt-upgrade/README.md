# nightly-ansible-apt-upgrade-scheduler

Utility that runs an `apt update && apt upgrade` on Debian/Ubuntu hosts and sends a whimsical apocalypse‑themed notification email.

## Usage

```bash
ansible-playbook -i inventory.ini src/apt_upgrade.yml
```

## Variables

- `notification_email` (default: `root@localhost`)
- `apocalypse_quote` (optional) – custom quote to include in the email body.

## What it does

1. Updates the apt cache.
2. Performs a full distribution upgrade (including autoremove).
3. Sends an email with a fun quote so you know the world may be ending, but your packages are up‑to‑date.

## License

MIT
