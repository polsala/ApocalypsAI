## Nightly Ansible Log Parser

This utility provides an Ansible playbook designed to parse system logs, identify common error patterns, and generate a summary report. It's useful for quickly assessing the health of systems by highlighting potential issues.

### Features

*   Parses `/var/log/syslog` (or a configurable log file).
*   Identifies common error keywords (e.g., 'error', 'failed', 'warning', 'critical').
*   Counts occurrences of identified errors.
*   Generates a summary report.

### Usage

1.  **Prerequisites**: Ansible installed on your control node.
2.  **Inventory**: Create an `inventory.ini` file specifying the target hosts.
3.  **Run the playbook**:
    ```bash
    ansible-playbook -i inventory.ini log_parser.yml
    ```

### Customization

*   **Log File**: Modify the `log_file_path` variable in `log_parser.yml` to point to your desired log file.
*   **Error Keywords**: Update the `error_keywords` list in `log_parser.yml` to include or exclude specific terms.
*   **Report Location**: The report will be saved to `/tmp/ansible_log_summary.txt` on the control node by default. You can change this using the `report_path` variable.

### Testing

This playbook includes a basic test case that simulates log file content and verifies the output of the log parsing task.
