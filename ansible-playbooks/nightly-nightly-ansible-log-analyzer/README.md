# Nightly Ansible Log Analyzer

This utility provides an Ansible playbook to analyze system logs on remote hosts. It searches for predefined error patterns and generates a summary report of findings.

## Features

*   Searches for common error keywords (e.g., "ERROR", "WARN", "CRITICAL").
*   Configurable log file paths.
*   Generates a summary report with counts of each pattern found.
*   Designed to be run nightly or on demand.

## Prerequisites

*   Ansible installed on the control node.
*   SSH access to the target hosts.
*   Python 3.x on target hosts (for the `log_analyzer` script).

## Usage

1.  **Inventory File (`inventory.ini`)**: Update the `inventory.ini` file with your target host details.

    ```ini
    [servers]
    your_server_ip_or_hostname ansible_user=your_ssh_user
    ```

2.  **Variables (`vars/main.yml`)**: Customize the `vars/main.yml` file to define log file paths and patterns to search for.

    ```yaml
    log_files_to_analyze:
      - /var/log/syslog
      - /var/log/auth.log
      - /var/log/kern.log

    patterns_to_find:
      - name: "ERROR"
        regex: "ERROR"
      - name: "WARNING"
        regex: "WARN(ING)?"
      - name: "CRITICAL"
        regex: "CRITICAL"
      - name: "FAILED_LOGIN"
        regex: "Failed password for invalid user"
    ```

3.  **Run the Playbook**: Execute the playbook using the `ansible-playbook` command.

    ```bash
    ansible-playbook -i inventory.ini analyze_logs.yml
    ```

## Output

The playbook will output a summary report for each host, detailing the number of occurrences for each defined pattern in the specified log files. The report will be printed to the console.

## Testing

This playbook includes a basic test case using `molecule` (though not fully implemented here for brevity, the structure is shown). For a real-world scenario, you would use `molecule` to test against a simulated environment.

To run tests (assuming molecule is installed):

```bash
cd tests
molecule test
```
