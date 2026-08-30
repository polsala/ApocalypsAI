## Nightly Ansible Log Parser

This Ansible playbook is designed to parse system logs on remote hosts, identify common error and warning patterns, and generate a summary report.

### Features

*   Parses `/var/log/syslog` (or a configurable log file).
*   Identifies common error keywords (e.g., 'error', 'failed', 'critical').
*   Identifies common warning keywords (e.g., 'warning', 'deprecated', 'notice').
*   Generates a summary report with counts of errors and warnings.

### Usage

1.  **Inventory:** Ensure your `inventory.ini` file is correctly configured with the target hosts.
2.  **Playbook Execution:** Run the playbook using `ansible-playbook -i inventory.ini parse_logs.yml`.

### Customization

*   **`log_file` variable:** Modify the `vars/main.yml` file to change the log file path.
*   **`error_patterns` and `warning_patterns` variables:** Update these lists in `vars/main.yml` to customize the keywords and regular expressions used for pattern matching.

### Testing

This playbook includes a basic test case using `molecule` (though not fully implemented in this example for brevity, the structure is present). For a real-world scenario, you would use `molecule` to test against a simulated environment.

**Mock Rationale:** The provided tests are conceptual and would typically involve mocking Ansible's execution environment or using a test VM. For this example, we'll simulate the output of the `command` module to demonstrate test logic.
