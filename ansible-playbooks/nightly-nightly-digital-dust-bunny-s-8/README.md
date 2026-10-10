# Nightly Digital Dust Bunny Sweeper

## Overview

The `nightly-digital-dust-bunny-sweeper` is an Ansible playbook designed to keep your servers tidy by automatically identifying and removing old, temporary files and caches – affectionately dubbed "digital dust bunnies." It helps reclaim disk space and maintain system hygiene across your infrastructure.

## Features

*   **Configurable Paths**: Specify which directories to scan for old files.
*   **Age-Based Cleanup**: Define how old a file must be before it's considered a "dust bunny" and swept away.
*   **Idempotent**: Running the playbook multiple times will only remove files that meet the criteria.
*   **Check Mode Support**: Safely preview what files *would* be removed without making actual changes.

## Requirements

*   Ansible (version 2.9 or newer recommended)
*   SSH access to target servers with appropriate permissions to read and delete files in the specified `cleanup_paths`.

## Usage

1.  **Define your Inventory**: Create or update `src/inventory.ini` with the hosts you want to clean.

    ```ini
    # src/inventory.ini
    [servers]
    webserver1.example.com
    dbserver.example.com

    [all:vars]
    ansible_user=your_ssh_user
    ansible_ssh_private_key_file=~/.ssh/id_rsa
    # Or use ansible_password if not using keys
    ```

2.  **Configure Cleanup Variables**: Edit `src/vars/main.yml` to specify the directories to clean and the age threshold.

    ```yaml
    # src/vars/main.yml
    cleanup_age_days: 30 # Files older than 30 days will be removed
    cleanup_paths:
      - /tmp
      - /var/tmp
      - /var/log/old_app_logs
      - /home/*/cache
    ```

3.  **Run in Check Mode (Recommended First!)**: Always run with `--check` first to see what changes the playbook *would* make.

    ```bash
    ansible-playbook -i src/inventory.ini src/playbook.yml --check --diff
    ```

    Review the output carefully. It will show you which files are identified as dust bunnies and would be removed.

4.  **Execute the Cleanup**: Once you are confident with the `--check` output, run the playbook without `--check` to perform the actual cleanup.

    ```bash
    ansible-playbook -i src/inventory.ini src/playbook.yml
    ```

## Variables

*   `cleanup_age_days` (default: `30`): Integer. Files older than this many days will be removed.
*   `cleanup_paths` (default: `['/tmp', '/var/tmp']`): List of strings. Directories to scan for old files. Supports glob patterns (e.g., `/home/*/cache`).

## Testing

To run the automated tests for this utility, navigate to the utility's root directory and execute the test playbook:

```bash
ansible-playbook tests/test_dust_bunny_sweeper.yml
```

This test creates a temporary directory, populates it with files of varying ages, runs the main playbook in `--check` mode against this controlled environment, and asserts that only the expected "old" files are marked for removal.
