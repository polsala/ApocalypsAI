# Ansible Log Parser Utility

This utility provides an Ansible playbook designed to parse system logs and identify common error patterns. It aims to offer a quick overview of potential issues without requiring deep manual log inspection.

## Features

*   Parses common log files (e.g., `/var/log/syslog`, `/var/log/auth.log`).
*   Identifies predefined error keywords (e.g., `ERROR`, `WARN`, `CRITICAL`, `failed`).
*   Summarizes the frequency of identified error patterns.
*   Outputs a human-readable report.

## Usage

1.  **Inventory File (`inventory.ini`)**: Ensure your `inventory.ini` file correctly lists the target hosts.
    ```ini
    [servers]
    your_server_ip ansible_user=your_user
    ```

2.  **Playbook Execution**: Run the playbook using `ansible-playbook`.
    ```bash
    ansible-playbook -i inventory.ini src/parse_logs.yml
    ```

## Output

The playbook will generate a summary report on the control node, detailing the count of each identified error keyword across the target hosts.

## Customization

The `vars/log_config.yml` file allows you to customize:

*   `log_files_to_parse`: A list of log file paths to scan.
*   `error_keywords`: A list of keywords to search for in the logs.
*   `report_output_path`: The path on the control node where the summary report will be saved.
