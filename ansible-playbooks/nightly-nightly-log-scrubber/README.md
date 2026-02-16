# Nightly Log Scrubber

## Purpose

The `nightly-log-scrubber` is an Ansible playbook designed to automate the secure management and scrubbing of system logs. In the post-apocalyptic landscape, resource management is key, and this utility ensures that valuable disk space isn't consumed by stale logs while also maintaining basic privacy and security by setting appropriate file permissions.

## Features

-   **Directory Management**: Ensures specified log directories exist.
-   **Permission Hardening**: Sets secure `0640` permissions (read/write for owner, read for group `adm`, no access for others) on all identified log files.
-   **Age-Based Deletion**: Identifies and deletes log files older than a configurable retention period.

## Usage

1.  **Inventory**: Ensure your `inventory.ini` file lists the target hosts where you want to run the log scrubber. For local execution, use `localhost` with `ansible_connection=local`.

    ```ini
    [local]
    localhost ansible_connection=local
    ```

2.  **Configuration**: Modify `src/vars/main.yml` to define the log paths to scan and the retention period in days.

    ```yaml
    # src/vars/main.yml
    log_paths:
      - /var/log
      - /var/log/nginx
      - /var/log/apache2
    log_retention_days: 30 # Delete logs older than 30 days
    ```

3.  **Run the Playbook**: Execute the playbook using `ansible-playbook`.

    ```bash
    ansible-playbook -i src/inventory.ini src/log_scrubber.yml
    ```

    Add `--check` and `--diff` flags for a dry run to see what changes would be made without actually applying them:

    ```bash
    ansible-playbook -i src/inventory.ini src/log_scrubber.yml --check --diff
    ```

## Automated Tests

The utility includes a self-contained test playbook (`tests/test_log_scrubber.yml`) that runs against `localhost` using temporary files to simulate log scenarios. This ensures the scrubber's logic for deletion and permission setting works as expected without affecting your actual system logs.

To run the tests:

```bash
ansible-playbook -i src/inventory.ini tests/test_log_scrubber.yml
```

The test playbook will:
1.  Create a temporary directory.
2.  Generate mock log files: one recent, one old (to be deleted), and one with incorrect permissions (to be corrected).
3.  Execute the main `log_scrubber.yml` playbook against this temporary directory.
4.  Assert that the old log file is deleted, the recent log file remains, and all remaining log files have the correct `0640` permissions.
5.  Clean up the temporary directory.
