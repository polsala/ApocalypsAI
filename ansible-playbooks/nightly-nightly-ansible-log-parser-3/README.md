## Nightly Ansible Log Parser

This utility provides an Ansible playbook designed to parse system logs, identify common error patterns, and generate a summary report. It's useful for quickly getting an overview of system health and potential issues.

### Features

*   Parses common log files (e.g., `/var/log/syslog`, `/var/log/auth.log`).
*   Identifies specific error keywords (e.g., 'error', 'failed', 'warning', 'denied').
*   Counts occurrences of identified errors.
*   Generates a summary report.

### Usage

1.  **Inventory File**: Ensure your `inventory.ini` file is correctly configured with the target hosts.
2.  **Playbook Execution**: Run the playbook using `ansible-playbook -i inventory.ini log_parser.yml`.

### Customization

*   **Log Files**: Modify the `log_files` variable in `vars/main.yml` to include or exclude specific log paths.
*   **Error Keywords**: Update the `error_keywords` variable in `vars/main.yml` to tailor the error detection.
*   **Report Template**: Customize the `templates/log_summary.j2` file to change the output format of the summary report.

### Testing

This playbook includes basic tests using Ansible's built-in testing capabilities. To run the tests, navigate to the `tests` directory and execute `ansible-playbook test_log_parser.yml`.
