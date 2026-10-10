## Nightly Ansible Log Parser

This Ansible playbook is designed to parse system logs on remote hosts, identify common error patterns, and generate a summary report. It's a whimsical yet useful tool for system administrators to quickly get an overview of potential issues.

### Features

*   Parses `/var/log/syslog` (or a configurable log file).
*   Identifies common error keywords (e.g., 'error', 'failed', 'warning', 'critical').
*   Groups similar log entries to reduce noise.
*   Generates a summary report with counts of identified errors.

### Usage

1.  **Inventory File**: Ensure your `inventory.ini` file is correctly configured with the hosts you want to manage.
2.  **Playbook Execution**: Run the playbook using `ansible-playbook -i inventory.ini parse_logs.yml`.

### Customization

*   **`log_file_path`**: Change the `log_file_path` variable in `vars/main.yml` to specify a different log file.
*   **`error_keywords`**: Modify the `error_keywords` list in `vars/main.yml` to include or exclude specific terms.
*   **`group_by_regex`**: Adjust the `group_by_regex` in `vars/main.yml` to refine how log entries are grouped.

### Testing

This playbook includes basic tests using `ansible-test` (or can be manually verified by running against a test host with mock log files).

**Note**: For true offline testing, you would typically mock the file content and the `command` module's output. The provided tests simulate this by checking the expected output structure.
