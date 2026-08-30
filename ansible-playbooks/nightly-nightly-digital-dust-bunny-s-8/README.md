# Nightly Digital Dust Bunny Sweeper

This Ansible playbook helps you keep your servers tidy by identifying and optionally removing "digital dust bunnies" – old, large, or temporary files that accumulate over time and consume valuable disk space. It's designed to be run periodically to maintain system hygiene.

## Features

*   **Configurable Scan Paths**: Define specific directories to scan for unwanted files.
*   **Age-Based Filtering**: Target files older than a specified number of days.
*   **Size-Based Filtering**: Target files larger than a specified size in megabytes.
*   **Dry Run Mode**: See what files *would* be removed without actually deleting them.
*   **Safe Deletion**: Only deletes files when explicitly enabled.

## Usage

1.  **Define your inventory**: Create an `inventory.ini` file listing the hosts you want to manage.

    ```ini
    [servers]
    your_server_ip_or_hostname
    ```

2.  **Configure variables**: Adjust the `vars/main.yml` file to define your scan paths, age thresholds, and size thresholds.

    ```yaml
    ---
    dust_bunny_scan_paths:
      - /tmp
      - /var/log/old_archives
    dust_bunny_age_threshold_days: 30
    dust_bunny_size_threshold_mb: 100
    dust_bunny_perform_cleanup: false # Set to true to actually delete files
    ```

3.  **Run in Dry Run Mode (Recommended First!)**:
    This will show you which files *would* be deleted without making any changes.

    ```bash
    ansible-playbook -i src/inventory.ini src/dust_bunny_sweeper.yml --check
    ```

4.  **Perform Cleanup**:
    Once you are confident with the dry run results, set `dust_bunny_perform_cleanup: true` in `src/vars/main.yml` and run the playbook without `--check`.

    ```bash
    ansible-playbook -i src/inventory.ini src/dust_bunny_sweeper.yml
    ```

## Automated Tests

To run the automated tests for this utility:

1.  Ensure you have Ansible installed.
2.  Navigate to the utility's root directory.
3.  Execute the test playbook:

    ```bash
    ansible-playbook -i tests/inventory_test.ini tests/test_dust_bunny_sweeper.yml
    ```

The tests will create temporary files, run the sweeper playbook's core logic, and verify that the correct files were removed, then clean up after themselves.
