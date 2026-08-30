# Nightly Ansible Digital Garden Trimmer

This Ansible playbook helps maintain a tidy digital environment by pruning old log files and clearing temporary directories. Think of it as a diligent gardener, trimming away the digital weeds and fallen leaves to keep your servers healthy and efficient.

## Features

*   **Log File Pruning**: Deletes log files older than a specified number of days from configured directories.
*   **Temporary Directory Clearing**: Empties the contents of specified temporary directories.
*   **Configurable**: Easily adjust paths and age thresholds via `vars/garden_config.yml`.

## Usage

1.  **Define your inventory**:
    Create an `inventory.ini` file listing the hosts you want to manage. For local execution, you can use:
    ```ini
    [local]
    localhost ansible_connection=local
    ```

2.  **Configure your garden**:
    Edit `vars/garden_config.yml` to specify which log directories to prune and which temporary directories to clear, along with the age threshold for log files.

    ```yaml
    # vars/garden_config.yml
    log_paths_to_trim:
      - /var/log/myapp
      - /var/log/nginx
    log_age_days: 30 # Delete log files older than 30 days

    temp_paths_to_clear:
      - /tmp/myapp_cache
      - /var/tmp/old_sessions
    ```

3.  **Run the playbook**:
    Execute the playbook using `ansible-playbook`:

    ```bash
    ansible-playbook -i src/inventory.ini src/trim_garden.yml
    ```

    For a dry run (to see what *would* be done without making changes):

    ```bash
    ansible-playbook -i src/inventory.ini src/trim_garden.yml --check
    ```

## Automated Tests

The tests for this utility are written in Python and use `subprocess` to run the Ansible playbook against a controlled, temporary local filesystem environment.

To run the tests:

1.  Ensure Ansible is installed.
2.  Navigate to the utility's root directory.
3.  Execute the test script:

    ```bash
    python3 tests/test_trim_garden.py
    ```

The tests will create a temporary directory, populate it with mock files (some old, some new), run the playbook, and then verify that only the expected old files were removed.
