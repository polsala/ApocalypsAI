# Apt Cleanup Playbook

This Ansible playbook simulates `apt-get autoremove --dry-run` on Debian/Ubuntu hosts, captures the output, and writes a markdown report to `/tmp/apt_cleanup_report.md`. Useful for auditing orphaned packages without making changes.

## Usage

```sh
ansible-playbook -i inventory.ini src/apt_cleanup.yml
```

The playbook runs with `become` privileges. After execution, view the report:

```sh
cat /tmp/apt_cleanup_report.md
```

## How it works

1. Runs a harmless `echo` command that mimics the output of `apt-get autoremove --dry-run`.
2. Stores the output in a variable.
3. Writes the output to a markdown file.

## Testing

Run the included test playbook:

```sh
ansible-playbook -i inventory.ini tests/test_apt_cleanup.yml
```

The test ensures the report file is created and non‑empty.
