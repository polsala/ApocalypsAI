# Nightly Digital Garden Pruner

## Overview

The `nightly-digital-garden-pruner` is an Ansible playbook designed to keep your servers (your 'digital gardens') tidy and efficient. It automates common cleanup tasks such as removing unused packages, clearing package manager caches, and deleting old temporary files. This helps free up disk space, reduce potential security risks from stale software, and maintain overall system health.

## Features

*   **Package Cleanup**: Removes orphaned packages and cleans package manager caches (supports `apt` for Debian/Ubuntu and `yum` for CentOS/RHEL).
*   **Temporary File Pruning**: Deletes files older than a configurable threshold from common temporary directories (`/tmp`, `/var/tmp`).
*   **Idempotent**: Can be run multiple times without causing unintended side effects.
*   **Configurable**: Easily adjust cleanup parameters via `vars/pruning_config.yml`.

## Requirements

*   **Ansible**: Version 2.9 or higher.
*   **Target Hosts**: Linux servers (Debian/Ubuntu or CentOS/RHEL based).
*   **Privileges**: The Ansible user must have `sudo` access on the target hosts to perform package management and file deletion tasks.

## Usage

1.  **Define your inventory**: Create an `inventory.ini` file listing your target servers.

    ```ini
    [webservers]
    web1.example.com
    web2.example.com

    [databases]
    db1.example.com
    ```

2.  **Configure pruning parameters (optional)**: Review and modify `vars/pruning_config.yml`.

    ```yaml
    # vars/pruning_config.yml
    pruning_temp_days_old: 7 # Delete temporary files older than 7 days
    pruning_paths:
      - /tmp
      - /var/tmp
    # Add more paths if needed, e.g., for specific application caches
    ```

3.  **Run the playbook**: Execute the playbook from your control machine.

    ```bash
    ansible-playbook -i inventory.ini src/prune_garden.yml
    ```

    To run in **check mode** (simulate without making changes):

    ```bash
    ansible-playbook -i inventory.ini src/prune_garden.yml --check
    ```

## Playbook Structure

*   `src/prune_garden.yml`: The main playbook containing all cleanup tasks.
*   `src/inventory.ini`: An example inventory file.
*   `src/vars/pruning_config.yml`: Variables to customize pruning behavior.
*   `tests/test_prune_garden.yml`: Automated tests for the playbook's core logic.
*   `tests/inventory_test.ini`: Inventory for testing.
