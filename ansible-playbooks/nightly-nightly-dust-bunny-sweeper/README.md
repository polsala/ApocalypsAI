# Nightly Digital Dust Bunny Sweeper

## Summary

This Ansible playbook, affectionately known as the "Digital Dust Bunny Sweeper," is designed to help you maintain a clean and tidy server environment. It automates the removal of old log files, temporary files, and clears package manager caches, ensuring your systems remain light, efficient, and free from digital clutter.

## Whimsical Purpose

Even in the post-apocalyptic digital age, servers accumulate digital dust bunnies – those forgotten files and caches that silently consume disk space and resources. This utility acts as your automated broom, sweeping away these invisible nuisances with a touch of whimsy, making your systems feel lighter and brighter.

## Features

*   **Log File Tumbleweed Removal**: Deletes log files older than a configurable number of days from specified directories.
*   **Temporary File Cobweb Clearing**: Removes temporary files older than a configurable number of days from common temporary directories.
*   **Package Cache Dusting**: Cleans up package manager caches (supports `apt` and `yum`/`dnf`) to free up space.
*   **Configurable Paths and Retention**: Easily adjust which directories are cleaned and how long files are retained via `vars/main.yml`.

## Usage

1.  **Prerequisites**:
    *   Ansible installed on your control machine.
    *   SSH access to your target servers with `sudo` privileges.

2.  **Inventory**: Update the `src/inventory.ini` file with the IP addresses or hostnames of the servers you wish to clean. For example:
    ```ini
    [webservers]
    web1.example.com
    web2.example.com

    [databases]
    db1.example.com
    ```
    Or, for local execution:
    ```ini
    [servers]
    localhost ansible_connection=local
    ```

3.  **Configuration**: Review and modify the `vars/main.yml` file to set your desired retention periods and target directories:
    ```yaml
    ---
    log_retention_days: 30 # Delete log files older than 30 days
    tmp_retention_days: 7  # Delete temporary files older than 7 days
    log_paths:
      - /var/log
      - /var/log/nginx # Add custom log paths here
    tmp_paths:
      - /tmp
      - /var/tmp
    ```

4.  **Run the Playbook**: Execute the playbook from your control machine:
    ```bash
    ansible-playbook -i src/inventory.ini src/dust_bunny_sweeper.yml
    ```

5.  **Dry Run (Check Mode)**: It's highly recommended to perform a dry run first to see what changes would be made without actually executing them:
    ```bash
    ansible-playbook -i src/inventory.ini src/dust_bunny_sweeper.yml --check --diff
    ```

## Automated Tests

To ensure the Digital Dust Bunny Sweeper works as intended, a self-contained test playbook is provided. These tests create a temporary, isolated environment, populate it with mock "old" and "new" files, run the main sweeper playbook against this mock environment, and then verify that only the "old" files have been removed.

### Running Tests

1.  Navigate to the utility's root directory.
2.  Execute the test playbook:
    ```bash
    ansible-playbook -i tests/inventory_test.ini tests/test_dust_bunny_sweeper.yml
    ```

### Test Rationale

Tests are designed to be deterministic and offline. They achieve this by:

*   **Local Connection**: All tasks run on `localhost` using `ansible_connection=local`.
*   **Isolated Environment**: A unique temporary directory is created for each test run (`/tmp/ansible_test_dust_bunny_sweeper_<timestamp>`).
*   **Mock Data**: `command` and `file` modules are used to create dummy "old" and "new" files within the temporary directories. File timestamps are set relative to the current date using `ansible_date_time.date` to ensure consistent "age" for files.
*   **Targeted Execution**: The main `dust_bunny_sweeper.yml` playbook is included and its `log_paths` and `tmp_paths` variables are overridden to point to the mock directories.
*   **Verification**: The `stat` module is used to deterministically check for the presence or absence of specific files in the mock environment after the sweeper has run.
*   **Cleanup**: The temporary test directory is removed at the end of the test run, leaving no trace on the host system.

This approach ensures that tests are repeatable, do not require network access to remote hosts, and do not interfere with the actual system's files.
