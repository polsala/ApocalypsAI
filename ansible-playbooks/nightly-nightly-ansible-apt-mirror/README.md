# nightly-ansible-apt-mirror

**Purpose**: Mirror a Debian/Ubuntu APT repository to a local directory using `apt-mirror`. This is handy for creating an offline package cache that can survive network outages—or the end of the world.

## Features

- Installs `apt-mirror` if missing.
- Generates a minimal `mirror.list` based on a user‑provided source URL.
- Runs `apt-mirror` to download packages.
- All tasks are idempotent; re‑run the playbook to update the mirror.

## Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `apt_mirror_source` | `"http://archive.ubuntu.com/ubuntu"` | Base URL of the repository to mirror. |
| `apt_mirror_distribution` | `"focal"` | Distribution codename (e.g., `focal`, `buster`). |
| `apt_mirror_components` | `["main", "restricted", "universe", "multiverse"]` | Repository components to include. |
| `apt_mirror_target_dir` | `"/var/spool/apt-mirror"` | Destination directory for the mirrored files. |

## Example Playbook

```yaml
- hosts: mirror
  become: true
  vars:
    apt_mirror_source: "http://archive.ubuntu.com/ubuntu"
    apt_mirror_distribution: "focal"
    apt_mirror_components:
      - main
      - restricted
      - universe
      - multiverse
    apt_mirror_target_dir: "/opt/apt-mirror"
  roles:
    - { role: nightly-ansible-apt-mirror }
```

## Running the Playbook Directly

```bash
ansible-playbook -i inventory.ini src/apt_mirror.yml \
  -e "apt_mirror_source=http://archive.ubuntu.com/ubuntu" \
  -e "apt_mirror_distribution=focal" \
  -e "apt_mirror_target_dir=/opt/apt-mirror"
```

## Testing

The `tests/` directory contains an Ansible test playbook that runs the main playbook in **check mode** to verify syntax and idempotency without touching the system.

```bash
ansible-playbook -i localhost, -c local tests/test_apt_mirror.yml
```

---

*Enjoy your offline package apocalypse!*
