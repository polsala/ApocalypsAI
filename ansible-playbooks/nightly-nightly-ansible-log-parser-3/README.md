## Nightly Ansible Log Parser

This utility provides an Ansible playbook designed to parse and analyze system logs on remote hosts. It can identify specific patterns, count occurrences, and report on potential anomalies.

### Features

*   Parses log files (e.g., `/var/log/syslog`, `/var/log/auth.log`).
*   Configurable patterns to search for (e.g., error messages, security events).
*   Counts occurrences of matched patterns.
*   Generates a summary report.

### Usage

1.  **Inventory File (`inventory.ini`)**: Define your target hosts.
    ```ini
    [webservers]
    server1.example.com
    server2.example.com
    ```

2.  **Playbook (`parse_logs.yml`)**: Customize the `log_patterns` variable to define what you want to search for.

3.  **Run the Playbook**: Execute the playbook using `ansible-playbook`.
    ```bash
    ansible-playbook -i inventory.ini parse_logs.yml
    ```

### Customization

The `parse_logs.yml` playbook has a `vars` section where you can modify:

*   `log_files`: A list of log file paths to parse.
*   `log_patterns`: A dictionary where keys are descriptive names for patterns and values are the regular expressions to search for.
*   `report_output_path`: The local path where the summary report will be saved.

### Testing

This playbook includes a basic test case using `molecule` (though the provided test is a simplified mock for demonstration). To run tests:

```bash
# Assuming you have molecule installed and configured
molecule test
```

### Example `log_patterns`

```yaml
log_patterns:
  "ERROR messages": "ERROR"
  "Failed logins": "Failed password for"
  "Critical events": "CRITICAL"
```
