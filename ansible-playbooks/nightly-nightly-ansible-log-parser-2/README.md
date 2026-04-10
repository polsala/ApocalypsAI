# Ansible Log Parser

This utility provides an Ansible playbook to parse system logs for specific patterns and generate reports. It's designed to be flexible and customizable, allowing you to define your own rules for log analysis.

## Features

*   Parses log files on remote hosts.
*   Supports customizable regex patterns for log matching.
*   Generates a summary report of matched log entries.
*   Can be extended to trigger alerts or actions based on log content.

## Prerequisites

*   Ansible installed on the control node.
*   SSH access to the target hosts.
*   The `regex` module (usually included with Ansible).

## Usage

1.  **Inventory File (`inventory.ini`)**: Define your target hosts.
    ```ini
    [servers]
    your_server_ip_or_hostname ansible_user=your_ssh_user
    ```

2.  **Log Patterns (`vars/log_patterns.yml`)**: Define the patterns to search for.
    ```yaml
    log_patterns:
      - name: "Critical Errors"
        path: "/var/log/syslog"
        regex: "ERROR.*critical"
        severity: "high"
      - name: "Failed Logins"
        path: "/var/log/auth.log"
        regex: "Failed password for invalid user"
        severity: "medium"
    ```

3.  **Run the Playbook**: Execute the playbook using `ansible-playbook`.
    ```bash
    ansible-playbook -i inventory.ini src/parse_logs.yml
    ```

## Customization

*   **`vars/log_patterns.yml`**: Add, remove, or modify log patterns. Each pattern requires a `name`, `path` to the log file, and a `regex` to match. An optional `severity` field can be added for reporting.
*   **`src/parse_logs.yml`**: Modify the playbook to change how results are handled (e.g., sending emails, writing to a different file, integrating with other systems).

## Testing

This playbook includes a basic test case using `molecule` (though not fully implemented in this example for brevity, it demonstrates the concept). For a real-world scenario, you would set up a test environment with mock log files.

### Test Scenario (Conceptual)

1.  Create a mock log file on a test host.
2.  Define a pattern to match specific lines in the mock log.
3.  Run the playbook against the test host.
4.  Verify that the playbook correctly identifies and reports the matched lines.
