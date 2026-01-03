# Nightly Digital Dust Bunny Sweeper

## Overview

The `nightly-digital-dust-bunny-sweeper` is an Ansible playbook designed to help maintain clean and efficient remote servers by identifying and optionally removing old, unused files and directories. Think of it as a digital vacuum cleaner, sweeping away the 'dust bunnies' that accumulate over time and consume valuable disk space.

It operates in a safe, configurable manner, allowing for dry runs to preview changes before any actual deletion occurs.

## Features

*   **Configurable Paths**: Specify multiple directories to scan for old files.
*   **Age Threshold**: Define how old a file or directory must be to be considered a 'dust bunny'.
*   **Dry Run Mode**: Safely preview what would be deleted without making any actual changes.
*   **Detailed Reporting**: Get a clear list of all identified old items.
*   **Idempotent**: Running the playbook multiple times with the same settings will yield the same result (after initial cleanup).

## Usage

1.  **Prepare your Inventory**: Ensure your `inventory.ini` file lists the target servers where you want to sweep for dust bunnies.

    ```ini
    [webservers]
    server1.example.com
    server2.example.com

    [databases]
    db1.example.com

    [all:vars]
    ansible_user=your_user
    ansible_ssh_private_key_file=~/.ssh/id_rsa
    ```

2.  **Configure Variables**: Modify `vars/main.yml` or pass variables via the command line (`-e`) to customize the sweep.

    ```yaml
    # vars/main.yml
    ---
    paths_to_sweep:
      - /tmp
      - /var/log/old_app_logs
      - /opt/temp_builds

    age_threshold_days: 30 # Items older than 30 days will be considered dust bunnies

    dry_run: true # Set to 'false' to actually remove files. Default is true for safety.
    ```

3.  **Run the Playbook (Dry Run - Recommended First!)**:

    To see what would be cleaned up without making any changes:

    ```bash
    ansible-playbook -i inventory.ini dust_bunny_sweeper.yml
    # Or explicitly:
    ansible-playbook -i inventory.ini dust_bunny_sweeper.yml -e "dry_run=true"
    ```

4.  **Run the Playbook (Actual Cleanup)**:

    Once you are satisfied with the dry run report, set `dry_run` to `false` to perform the actual cleanup:

    ```bash
    ansible-playbook -i inventory.ini dust_bunny_sweeper.yml -e "dry_run=false"
    ```

## Configuration Variables

*   `paths_to_sweep` (list of strings, **required**):
    A list of absolute paths on the remote server where the playbook should look for old files and directories. Example: `['/tmp', '/var/log/old_app_logs']`.

*   `age_threshold_days` (integer, **required**):
    The number of days. Any file or directory with a modification time older than this threshold will be considered a 'dust bunny'. Example: `30`.

*   `dry_run` (boolean, **optional**, default: `true`):
    If `true`, the playbook will only report what *would* be deleted. If `false`, it will actually remove the identified files and directories. **Always start with `dry_run: true`!**

## Requirements

*   Ansible (version 2.9 or newer recommended)
*   SSH access to target servers
*   Sufficient permissions on target servers to read and delete files in `paths_to_sweep`.
