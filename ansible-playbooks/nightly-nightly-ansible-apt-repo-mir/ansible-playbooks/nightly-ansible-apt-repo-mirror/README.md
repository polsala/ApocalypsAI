# nightly-ansible-apt-repo-mirror

## Overview

`nightly-ansible-apt-repo-mirror` is a whimsical yet practical Ansible playbook that synchronises a remote Debian/Ubuntu APT repository to a local directory.  This enables teams to create an offline package cache – perfect for post‑apocalypse environments, CI runners without internet access, or simply speeding up repeated installations.

## Features

- Idempotent: creates the target directory only if it does not exist.
- Uses `rsync` (or any command you prefer) to mirror the repository.
- Supports custom mirror URLs and destination paths via extra variables.
- Dry‑run (`--check`) safe – no files are created during testing.

## Requirements

- Ansible 2.9+ installed on the control node.
- `rsync` available on the target host (the host where the mirror will be stored).

## Usage

```bash
# Clone the repository (or copy the folder into your own playbooks directory)
git clone https://github.com/polsala/ApocalypsAI.git
cd ansible-playbooks/nightly-ansible-apt-repo-mirror

# Run the playbook (replace variables as needed)
ansible-playbook -i inventory.ini src/main.yml \
  -e "mirror_url=http://archive.ubuntu.com/ubuntu" \
  -e "local_path=/opt/apt-mirror"
```

### Dry‑run (check mode)

```bash
ansible-playbook -i inventory.ini src/main.yml \
  -e "mirror_url=http://archive.ubuntu.com/ubuntu" \
  -e "local_path=/opt/apt-mirror" \
  --check
```

The dry‑run will report what would happen without actually creating directories or transferring data.

## Inventory

A minimal `inventory.ini` is provided that targets `localhost` for quick testing:

```ini
[local]
localhost ansible_connection=local
```

## Testing

Automated tests are located in the `tests/` directory and can be executed with:

```bash
ansible-playbook -i inventory.ini tests/test_playbook.yml --check
```

The test ensures the playbook runs in check mode without side‑effects.
