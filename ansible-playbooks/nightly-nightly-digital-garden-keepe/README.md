# Nightly Digital Garden Keeper

## Summary

This Ansible playbook acts as your diligent digital gardener, ensuring your servers (your 'digital garden plots') are well-maintained. It performs essential tasks like 'watering' with system updates and 'weeding' by removing old logs and temporary files. After its nightly rounds, it generates a whimsical report detailing the 'harvest' – what was updated, cleaned, and generally tidied up.

## Features

*   **Watering (System Updates):** Updates package lists and upgrades all installed packages on Debian-based systems.
*   **Weeding (Cleanup):** Removes orphaned packages, cleans package caches, and purges old log files to free up space and reduce clutter.
*   **Harvest Report:** Generates a summary report of all actions taken, providing a whimsical overview of your garden's health.

## Prerequisites

*   Ansible installed on your control machine.
*   SSH access to your target servers with appropriate permissions (e.g., `sudo` access for package management).
*   Python installed on target servers (Ansible's default connection method).

## Usage

1.  **Define your inventory:** Create an `inventory.ini` file (or use an existing one) listing the servers you want to manage. Example:

    ```ini
    [garden_servers]
    server1.example.com
    server2.example.com
    ```

2.  **Configure variables (optional):** Review `src/vars/main.yml` to adjust settings like `log_retention_days`.

3.  **Run the playbook:**

    ```bash
    ansible-playbook -i src/inventory.ini src/garden_keeper.yml
    ```

    To run in check mode (dry run) and see what *would* be done:

    ```bash
    ansible-playbook -i src/inventory.ini src/garden_keeper.yml --check
    ```

    The generated report will be printed to standard output by default. You can redirect it to a file:

    ```bash
    ansible-playbook -i src/inventory.ini src/garden_keeper.yml > garden_report_$(date +%Y%m%d).txt
    ```

## Example `src/inventory.ini`

```ini
[garden_servers]
localhost ansible_connection=local
# server.example.com
# another.server.com
```

## Example `src/vars/main.yml`

```yaml
---
log_retention_days: 30
log_paths_to_clean:
  - /var/log/*.log
  - /var/log/*/*.log
  - /var/log/nginx/*.log
```
