# Ansible Log Parser

This Ansible playbook is designed to parse system logs (e.g., `/var/log/syslog`, `/var/log/auth.log`) on remote hosts, identify common error patterns, and generate a summary report.

## Features

*   Parses specified log files.
*   Identifies common error keywords (e.g., 'error', 'failed', 'warning', 'denied').
*   Counts occurrences of identified patterns.
*   Generates a summary report on the target host.

## Prerequisites

*   Ansible installed on the control node.
*   SSH access to the target hosts.
*   The `ansible-core` package installed on the control node.

## Usage

1.  **Inventory File (`inventory.ini`)**: Ensure your `inventory.ini` file is correctly configured with the hosts you want to manage.

    ```ini
    [servers]
    your_server_ip_or_hostname ansible_user=your_ssh_user
    ```

2.  **Playbook Execution**: Run the playbook using the `ansible-playbook` command:

    ```bash
    ansible-playbook -i inventory.ini parse_logs.yml
    ```

    You can specify a different log file to parse using the `log_file_path` variable:

    ```bash
    ansible-playbook -i inventory.ini parse_logs.yml --extra-vars "log_file_path=/var/log/apache2/error.log"
    ```

## Playbook Structure

*   `parse_logs.yml`: The main Ansible playbook.
*   `tasks/main.yml`: Contains the core tasks for log parsing.
*   `templates/log_summary.j2`: Jinja2 template for generating the summary report.
*   `vars/main.yml`: Default variables, including common error patterns.
*   `tests/test_parse_logs.yml`: Molecule test for the playbook.
*   `tests/inventory_test.ini`: Inventory file for testing.
