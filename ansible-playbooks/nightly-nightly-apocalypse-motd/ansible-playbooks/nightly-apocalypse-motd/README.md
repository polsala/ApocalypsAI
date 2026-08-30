# Nightly Apocalypse MOTD

This Ansible playbook installs a random post-apocalyptic quote into a MOTD file each time it runs. It is whimsical, yet useful for adding a bit of flavor to server logins.

## Features
- Picks a random quote from a built-in list.
- Writes the quote to a configurable file (default `/etc/motd`).
- Fully idempotent – running it again will replace the file with a new quote.

## Requirements
- Ansible 2.9+ installed on the control machine.
- Target hosts reachable via SSH (the playbook defaults to `localhost`).

## Usage
```bash
ansible-playbook -i inventory.ini src/setup_motd.yml -e "motd_path=/etc/motd"
```

You can change `motd_path` to any writable location for testing, e.g.:
```bash
ansible-playbook -i inventory.ini src/setup_motd.yml -e "motd_path=/tmp/motd_test"
```

## License
MIT
