## Nightly Ansible Log Parser

This utility provides an Ansible playbook designed to parse system logs, identify common error patterns, and generate a summary report. It's useful for quickly assessing the health of systems by highlighting potential issues.

### Features

*   Parses `/var/log/syslog` (or a configurable log file).
*   Identifies common error keywords (e.g., 'error', 'failed', 'warning', 'critical').
*   Counts occurrences of identified errors.
*   Generates a summary report with the most frequent errors.

### Usage

1.  **Inventory File**: Create an `inventory.ini` file specifying the hosts to run the playbook on.
    ```ini
    [servers]
    your_server_ip_or_hostname
    ```

2.  **Run the Playbook**: Execute the playbook using `ansible-playbook`.
    ```bash
    ansible-playbook -i inventory.ini parse_logs.yml
    ```

3.  **Output**: The playbook will output a summary of the most common errors found in the logs to the console.

### Customization

*   **Log File**: Modify the `log_file_path` variable in `parse_logs.yml` to target a different log file.
*   **Error Keywords**: Update the `error_keywords` list in `parse_logs.yml` to include or exclude specific terms.

### Testing

This playbook includes a basic test case that mocks the log file content and verifies the expected output of the log parsing task.
