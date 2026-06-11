# Nightly Ansible Log Parser

This utility provides an Ansible playbook designed to parse system logs, identify common error patterns, and generate a summary report. It's useful for quickly assessing the health of systems by highlighting potential issues.

## Features

*   Parses `/var/log/syslog` (or a configurable log file).
*   Identifies common error keywords (e.g., "error", "failed", "warning", "critical").
*   Counts occurrences of identified errors.
*   Generates a summary report.

## Prerequisites

*   Ansible installed on the control node.
*   SSH access to the target hosts.
*   Sudo privileges on target hosts for reading log files (if necessary).

## Usage

1.  **Inventory File**: Ensure your `inventory.ini` file is correctly configured with the hosts you want to target.

    ```ini
    [servers]
    your_server_ip_or_hostname ansible_user=your_ssh_user
    ```

2.  **Run the Playbook**:

    ```bash
    ansible-playbook -i inventory.ini log_parser.yml
    ```

    The output will be displayed on your terminal, summarizing the log findings.

## Customization

*   **Log File Path**: Modify the `log_file_path` variable in `log_parser.yml` to point to a different log file.
*   **Error Keywords**: Update the `error_keywords` list in `log_parser.yml` to include or exclude specific terms.

## Testing

This playbook includes a basic test case using `molecule` (though the provided test is a simplified mock for demonstration purposes within this JSON structure). For a real-world scenario, you would use `molecule` to test against actual or simulated environments.

To run the provided mock test:

```bash
ansible-playbook -i tests/inventory_test.ini tests/test_log_parser.yml
```
