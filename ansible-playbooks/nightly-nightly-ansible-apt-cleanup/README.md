# nightly-ansible-apt-cleanup

Utility that provides an Ansible playbook to perform an automatic apt package cleanup on Debian/Ubuntu hosts. It runs `apt-get autoremove` in check mode by default and can be executed in real mode to free disk space.

## Usage

```sh
ansible-playbook -i inventory.ini apt_cleanup.yml
```

Run in check (dry‑run) mode:

```sh
ansible-playbook -i inventory.ini apt_cleanup.yml --check
```

The playbook gathers facts, ensures the host is Debian based, and runs the apt autoremove task.

## Test

```sh
cd tests && ./test_apt_cleanup.sh
```

The test script runs the playbook in check mode to verify that it executes without errors.
