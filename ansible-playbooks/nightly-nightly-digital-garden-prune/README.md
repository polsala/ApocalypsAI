# Nightly Digital Garden Pruner

## Summary
The `nightly-digital-garden-pruner` is an Ansible playbook designed to keep your servers' digital "gardens" healthy and tidy. It automates the process of removing digital "weeds" such as old kernels, orphaned packages, and stale temporary files, while also ensuring your package lists are updated and upgrades are applied. Think of it as a diligent digital gardener, ensuring your systems are lean, secure, and have ample space to flourish.

## Features
- **Package Updates**: Updates package lists and upgrades all installed packages.
- **Kernel Pruning**: Identifies and removes old, unused Linux kernels to free up disk space.
- **Orphaned Package Removal**: Automatically removes packages that were installed as dependencies but are no longer needed.
- **Temporary File Cleanup**: Cleans up stale files in common temporary directories (`/tmp`, `/var/tmp`).
- **Disk Usage Reporting**: Provides a summary of disk space before and after the pruning process.

## Prerequisites
- Ansible installed on your control machine.
- SSH access to your target servers with appropriate permissions (e.g., `sudo` access for package management).
- Python installed on target servers (Ansible's default connection method requires it).

## Usage

1.  **Define your inventory**:
    Create an `inventory.ini` file (or use an existing one) listing your target servers.

    ```ini
    [garden_servers]
    server1.example.com
    server2.example.com ansible_user=ubuntu
    ```

2.  **Run the playbook**:
    Execute the playbook using the `ansible-playbook` command.

    ```bash
    ansible-playbook -i inventory.ini prune_garden.yml --ask-become-pass
    ```
    (Use `--ask-become-pass` if your `sudo` requires a password, or configure passwordless sudo for the Ansible user.)

3.  **Review the report**:
    After execution, a pruning report will be generated and displayed in the console, summarizing the actions taken and disk space changes.

## Files

-   `prune_garden.yml`: The main playbook orchestrating all pruning tasks.
-   `inventory.ini`: Example inventory file.
-   `tasks/`: Directory containing modular tasks for different pruning operations.
    -   `update_packages.yml`: Handles `apt update` and `apt upgrade`.
    -   `clean_kernels.yml`: Removes old kernels.
    -   `clean_orphans.yml`: Runs `apt autoremove`.
    -   `clean_tmp.yml`: Cleans temporary directories.
-   `templates/pruning_report.j2`: Jinja2 template for the final pruning report.
-   `tests/`: Contains a test playbook to verify syntax and mock execution.

## Example Output (Console Report)

```
--- Digital Garden Pruning Report ---

Date: 2023-10-27 10:30:00

Host: server1.example.com

Disk Usage Before:
  Filesystem      Size  Used Avail Use% Mounted on
  /dev/sda1       100G   60G  40G  60% /

Pruning Actions:
- Packages updated and upgraded.
- Removed 2 old kernels.
- Orphaned packages removed: Yes
- Cleaned 2 files from /tmp.
- Cleaned 1 files from /var/tmp.

Disk Usage After:
  Filesystem      Size  Used Avail Use% Mounted on
  /dev/sda1       100G   58G  42G  58% /

--- End Report ---
```
