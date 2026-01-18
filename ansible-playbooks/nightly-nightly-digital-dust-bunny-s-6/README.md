# Nightly Digital Dust Bunny Sweeper

This Ansible playbook helps maintain server hygiene by identifying and optionally removing old, unused files and directories across your infrastructure. Think of it as a digital vacuum cleaner for your servers, sweeping away those pesky 'dust bunnies' that accumulate over time.

## Features

*   **Configurable Scan Paths**: Specify which directories to scan for old files.
*   **Age Threshold**: Define how old a file or directory must be to be considered a 'dust bunny'.
*   **Dry Run Mode**: Run the playbook to only report findings without performing any deletions.
*   **Cleanup Mode**: Enable actual deletion of identified 'dust bunnies'.

## Prerequisites

*   Ansible installed on your control machine.
*   SSH access to your target servers with appropriate permissions (e.g., `sudo` if cleaning system directories).
*   An Ansible inventory file (`inventory.ini`) defining your target hosts.

## Usage

1.  **Configure Variables**: 
    Edit `vars/main.yml` to set your desired `scan_paths`, `age_threshold_days`, and `cleanup_mode`.

    *   `scan_paths`: A list of absolute paths to directories you want to scan.
    *   `age_threshold_days`: An integer representing the minimum age (in days) for a file/directory to be considered for cleanup.
    *   `cleanup_mode`: Set to `false` for a dry run (report only), or `true` to actually delete files.

2.  **Prepare Inventory**: 
    Ensure your `inventory.ini` file lists the hosts you want to target.

    ```ini
    [webservers]
    web1.example.com
    web2.example.com

    [dbservers]
    db1.example.com

    [all:vars]
    ansible_user=your_ssh_user
    ansible_ssh_private_key_file=~/.ssh/id_rsa
    # ansible_become=true # Uncomment if sudo is required for cleanup
    ```

3.  **Run the Playbook (Dry Run - Recommended First!)**:
    Always start with `cleanup_mode: false` in `vars/main.yml` to see what *would* be removed.

    ```bash
    ansible-playbook -i inventory.ini dust_bunny_sweeper.yml
    ```

    This will output a report of all identified digital dust bunnies.

4.  **Run the Playbook (Cleanup Mode)**:
    Once you are confident with the dry run report, set `cleanup_mode: true` in `vars/main.yml`.

    ```bash
    ansible-playbook -i inventory.ini dust_bunny_sweeper.yml
    ```

    **WARNING**: Running in cleanup mode will permanently delete files. Use with caution and ensure you have backups.

## Configuration (`vars/main.yml`)

```yaml
---
# Default paths to scan for old files and directories
scan_paths:
  - /tmp
  - /var/log
  - /opt/old_data

# Age threshold in days. Files/directories older than this will be identified.
age_threshold_days: 60

# Set to 'true' to actually remove identified dust bunnies.
# Set to 'false' for a dry run (reporting only).
cleanup_mode: false
```

## Testing

To run the automated tests for this playbook, use the following command:

```bash
ansible-playbook -i tests/inventory_test.ini tests/test_dust_bunny_sweeper.yml
```

The tests use a mocked `find` module output to ensure deterministic and offline validation of the playbook's logic without actual filesystem interaction.
