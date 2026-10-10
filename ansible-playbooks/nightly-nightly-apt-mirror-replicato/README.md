# nightly-apt-mirror-replicator

Utility to mirror Debian/Ubuntu APT repositories to a local directory using `apt-mirror`. The playbook is fully configurable and includes a mockable command for offline testing.

## Usage

```bash
ansible-playbook -i inventory.ini src/apt_mirror.yml -e "repo_url='http://archive.ubuntu.com/ubuntu' mirror_dir='/opt/apt-mirror'"
```

## Variables

- `repo_url` (default: `http://archive.ubuntu.com/ubuntu`) – URL of the repository to mirror.
- `mirror_dir` (default: `/opt/apt-mirror`) – Local directory where the mirror will be stored.
- `apt_mirror_cmd` (default: `apt-mirror`) – Command to run; override with a mock command for testing.

## Testing

Run the provided test playbook which overrides `apt_mirror_cmd` with a harmless `touch` command:

```bash
ansible-playbook -i tests/inventory.ini tests/test_apt_mirror.yml
```
