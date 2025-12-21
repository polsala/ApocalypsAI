# Nightly Digital Dust Bunny Sweeper

## Summary

This Ansible playbook helps you keep your digital realms sparkling clean by identifying and optionally removing "digital dust bunnies" across your servers. It targets old files, empty directories, and broken symlinks, providing a whimsical report of its findings.

## Features

*   **Old File Detection**: Finds files older than a configurable age threshold.
*   **Empty Directory Identification**: Locates directories that contain no files or subdirectories.
*   **Broken Symlink Discovery**: Identifies symbolic links that point to non-existent targets.
*   **Dry Run Mode**: Safely preview what would be cleaned without making any changes.
*   **Cleanup Mode**: Execute the cleanup to remove identified items.
*   **Whimsical Report**: Generates a "Digital Dust Bunny Report" detailing findings and actions.

## Prerequisites

*   Ansible (version 2.9 or newer recommended)
*   Access to target servers via SSH (configured in your Ansible inventory)

## Usage

1.  **Clone the repository** (if not already part of ApocalypsAI).

2.  **Navigate to the utility directory**:
    ```bash
    cd ansible-playbooks/nightly-digital-dust-sweeper
    ```

3.  **Configure your inventory**: Edit `inventory.ini` to list the servers you want to scan.
    ```ini
    # inventory.ini
    [servers]
    localhost ansible_connection=local
    # server1.example.com
    # server2.example.com
    ```

4.  **Configure variables**: Adjust `vars/main.yml` to define `scan_paths`, `old_file_age_days`, and `dry_run`.
    ```yaml
    # vars/main.yml
    ---
    # Paths to scan for digital dust bunnies
    scan_paths:
      - "/tmp"
      # - "/var/log"
      # - "{{ ansible_env.HOME }}/Downloads"

    # Age threshold for "old" files (in days)
    old_file_age_days: 30

    # Whether to actually remove files or just report (true for dry run, false for cleanup)
    dry_run: true
    ```

5.  **Run the playbook**:

    *   **Dry Run (Recommended First)**: To see what would be cleaned without making changes:
        ```bash
        ansible-playbook -i inventory.ini dust_bunny_sweeper.yml -e "dry_run=true"
        ```

    *   **Cleanup Run**: To actually remove the identified items:
        ```bash
        ansible-playbook -i inventory.ini dust_bunny_sweeper.yml -e "dry_run=false"
        ```

    After execution, a report will be generated at `/tmp/dust_bunny_report_<hostname>.txt` on each target server.

## Testing

To ensure the Digital Dust Bunny Sweeper works as expected, a comprehensive test playbook is provided. This test creates a controlled environment with mock "dust bunnies" and verifies the playbook's behavior in both dry-run and cleanup modes.

1.  **Navigate to the utility directory**:
    ```bash
    cd ansible-playbooks/nightly-digital-dust-sweeper
    ```

2.  **Run the tests**:
    ```bash
    ansible-playbook -i tests/inventory_test.ini tests/test_dust_bunny_sweeper.yml
    ```

    This will:
    *   Set up a temporary directory with old files, empty directories, and broken symlinks.
    *   Run the main playbook in `dry_run` mode and assert that no files are removed but the report is correct.
    *   Run the main playbook in `cleanup` mode and assert that all mock dust bunnies are removed and the report is correct.
    *   Clean up the temporary test environment.

## Contributing

Feel free to suggest improvements, new dust bunny types to sweep, or more whimsical report phrases!
