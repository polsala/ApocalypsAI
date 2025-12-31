## Nightly Ansible Log Parser

This Ansible playbook is designed to parse system logs on remote hosts, identify specific patterns, and generate a report of potential anomalies or interesting events.

### Features

*   **Log File Targeting**: Specify which log files to parse.
*   **Pattern Matching**: Define regular expressions to search for.
*   **Anomaly Detection**: Basic detection of repeated errors or unusual log entries.
*   **Reporting**: Generates a summary report of findings.

### Usage

1.  **Inventory**: Ensure your `inventory.ini` file is correctly configured with the target hosts.
2.  **Variables**: Modify `vars/log_analysis.yml` to define:
    *   `log_files`: A list of log file paths to analyze.
    *   `patterns`: A dictionary where keys are descriptive names for patterns and values are regular expressions.
    *   `anomaly_threshold`: The number of occurrences within a short period to consider an anomaly (e.g., 5).
3.  **Run the Playbook**: Execute the playbook using `ansible-playbook -i inventory.ini log_parser.yml`.

### Example `vars/log_analysis.yml`

```yaml
log_files:
  - /var/log/syslog
  - /var/log/auth.log

patterns:
  ssh_failed_login: "Failed password for invalid user"
  kernel_panic: "Kernel panic - not syncing"
  disk_full: "No space left on device"

anomaly_threshold: 5
```

### Testing

This playbook includes a basic test case using `molecule` (though not fully implemented in this example for brevity, it demonstrates the concept). The tests focus on ensuring the playbook runs without errors and that the log parsing logic is applied correctly.

To run tests (assuming molecule is installed):

```bash
molecule test -s default
```
