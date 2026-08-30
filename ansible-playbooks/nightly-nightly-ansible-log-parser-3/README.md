## Nightly Ansible Log Parser

This utility provides an Ansible playbook designed to parse system logs, identify common error patterns, and generate a summary report. It's useful for quickly getting an overview of system health and potential issues.

### Features

*   Parses `/var/log/syslog` (or a configurable log file).
*   Identifies common error keywords (e.g., 'error', 'fail', 'warn', 'critical').
*   Counts occurrences of identified errors.
*   Generates a summary report.

### Usage

1.  **Inventory:** Ensure your `inventory.ini` file is correctly configured with the target hosts.
2.  **Playbook Execution:** Run the playbook using `ansible-playbook -i inventory.ini parse_logs.yml`.

### Customization

You can customize the following variables in `vars/main.yml`:

*   `log_file_path`: The path to the log file to parse (default: `/var/log/syslog`).
*   `error_keywords`: A list of keywords to search for in the logs (default: `['error', 'fail', 'warn', 'critical']`).
*   `report_output_path`: The path where the summary report will be saved on the control node (default: `./log_summary_report.txt`).

### Testing

This playbook includes a basic test case using `molecule` (though for simplicity in this standalone example, we'll simulate the test output directly in the `tests/` directory).

**Note:** In a real-world scenario, you would use `molecule` to test this playbook against actual or mocked environments.
