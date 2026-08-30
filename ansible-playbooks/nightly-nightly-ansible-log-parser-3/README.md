# Ansible Log Parser

This Ansible playbook is designed to parse system logs on remote hosts, identify common error and warning patterns, and generate a summary report.

## Features

*   Parses `/var/log/syslog` (or a configurable log file).
*   Identifies common error keywords (e.g., "error", "failed", "warning", "critical").
*   Groups similar log entries to reduce noise.
*   Generates a summary report with counts of different log levels and common messages.

## Prerequisites

*   Ansible installed on the control node.
*   SSH access to the target hosts.
*   Python installed on target hosts (for the `loguru` dependency).

## Usage

1.  **Inventory File**: Ensure your `inventory.ini` file is correctly configured with your target hosts.

    ```ini
    [servers]
    your_server_ip_or_hostname ansible_user=your_ssh_user
    ```

2.  **Playbook Execution**: Run the playbook using the `ansible-playbook` command.

    ```bash
    ansible-playbook -i inventory.ini parse_logs.yml
    ```

3.  **Customization**: You can customize the log file path and error patterns by modifying the `vars/main.yml` file.

## Example Output (Summary Report)

```
Log Analysis Report for: your_server_ip_or_hostname
===================================================

Total Log Entries Processed: 1500

Summary by Level:
-----------------
ERROR: 50
WARNING: 120
INFO: 1330

Top 5 Common Error Messages:
----------------------------
1.  "Failed to connect to database": 15 times
2.  "Disk space critically low": 10 times
3.  "Authentication failed for user": 8 times
4.  "Service crashed unexpectedly": 7 times
5.  "Configuration error in module X": 5 times

Top 5 Common Warning Messages:
------------------------------
1.  "Deprecation warning for function Y": 25 times
2.  "High CPU usage detected": 20 times
3.  "Network latency increased": 15 times
4.  "Resource limit approaching": 10 times
5.  "Unused configuration parameter found": 8 times
```
