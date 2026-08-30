# Ansible Log Parser

This Ansible playbook is designed to parse system logs on remote hosts, identify common error and warning patterns, and generate a summary report.

## Features

*   Parses `/var/log/syslog` (or a configurable log file).
*   Identifies common error keywords (e.g., 'error', 'failed', 'critical').
*   Identifies common warning keywords (e.g., 'warning', 'deprecated', 'notice').
*   Generates a summary report with counts of errors and warnings.
*   Can be configured to target specific hosts or groups.

## Prerequisites

*   Ansible installed on the control node.
*   SSH access to the target hosts.
*   Python installed on target hosts (for the `logentries` module, if used, or for basic file operations).

## Usage

1.  **Inventory File**: Ensure your `inventory.ini` file is correctly configured with the hosts you want to target.

    ```ini
    [webservers]
    webserver1.example.com
    webserver2.example.com

    [dbservers]
dbserver1.example.com
    ```

2.  **Run the Playbook**:

    ```bash
    ansible-playbook -i inventory.ini log_parser.yml
    ```

    You can also specify a particular host group:

    ```bash
    ansible-playbook -i inventory.ini log_parser.yml --limit webservers
    ```

## Customization

*   **Log File Path**: Modify the `log_file_path` variable in `log_parser.yml` to point to your desired log file.
*   **Error/Warning Keywords**: Update the `error_keywords` and `warning_keywords` lists in `log_parser.yml` to customize the patterns you want to detect.
*   **Report Output**: The report is currently printed to the console. You can modify the `debug` task to save it to a file or send it via email using Ansible's `mail` module.

## Testing

This playbook includes a basic test using `ansible-lint` and a mock inventory. To run the tests:

1.  Install `ansible-lint`:
    ```bash
    pip install ansible-lint
    ```
2.  Run `ansible-lint` in the `ansible-playbooks/nightly-ansible-log-parser/` directory:
    ```bash
    ansible-lint log_parser.yml
    ```

For more in-depth testing, consider using Molecule for more complex scenarios.
