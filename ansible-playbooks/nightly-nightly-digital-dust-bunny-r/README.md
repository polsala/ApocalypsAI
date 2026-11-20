# Nightly Digital Dust Bunny Removal

## Summary
This Ansible playbook, affectionately named the "Digital Dust Bunny Removal" utility, is designed to keep your servers spick and span. It automates the cleanup of common temporary files, package manager caches, and old logs across various Linux distributions, ensuring optimal system performance and reclaiming disk space.

## Features
- Cleans APT cache on Debian/Ubuntu systems.
- Cleans YUM/DNF cache on RedHat-based systems.
- Removes temporary files older than 7 days from `/tmp` and `/var/tmp`.
- Trims systemd journal logs, keeping them tidy.

## Usage

### Prerequisites
- Ansible installed on your control machine.
- SSH access to your target servers with `sudo` privileges.

### 1. Inventory Setup
Create an `inventory.ini` file (or use an existing one) that lists the servers you want to clean. For example:

```ini
[webservers]
web1.example.com
web2.example.com

[databases]
db1.example.com

[all:vars]
ansible_user=your_ssh_user
ansible_become_user=root
ansible_become_method=sudo
```

### 2. Run the Playbook
Execute the playbook using the `ansible-playbook` command, specifying your inventory file:

```bash
ansible-playbook -i inventory.ini src/dust_bunny_cleanup.yml
```

If you want to run it only on specific hosts or groups, you can use the `--limit` flag:

```bash
ansible-playbook -i inventory.ini src/dust_bunny_cleanup.yml --limit webservers
```

### 3. Review Output
The playbook will provide output indicating which tasks were performed and if any changes were made. It's designed to be idempotent where possible, meaning running it multiple times will have the same effect as running it once.

## Testing

To ensure the dust bunnies are properly removed, a comprehensive test playbook is provided. This test creates dummy temporary files (some old, some new) and then verifies that only the old ones are removed after running the cleanup playbook.

### How to Run Tests

1.  Navigate to the utility's root directory.
2.  Run the test playbook against `localhost`:

    ```bash
    ansible-playbook -i tests/inventory_test.ini tests/test_dust_bunny_cleanup.yml
    ```

    This command will:
    - Create temporary test files in `/tmp` and `/var/tmp`.
    - Set modification times for some files to simulate "old" dust bunnies.
    - Execute the `dust_bunny_cleanup.yml` playbook.
    - Assert that the "old" files are gone and "new" files remain.
    - Clean up all test files and directories.

If the tests pass, you'll see a summary indicating success. If any assertions fail, it will provide details on what went wrong.
