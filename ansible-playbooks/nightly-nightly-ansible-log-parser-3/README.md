# Nightly Ansible Log Parser

This Ansible playbook is designed to parse system logs on remote hosts, identify critical events or potential anomalies, and generate a summarized report.

## Features

*   Parses common log file locations (e.g., `/var/log/syslog`, `/var/log/auth.log`).
*   Configurable keywords and patterns to search for (e.g., `ERROR`, `WARNING`, `failed login`).
*   Generates a summary report of found log entries.
*   Can be extended to include more sophisticated log analysis techniques.

## Usage

1.  **Inventory File**: Ensure your `inventory.ini` file is correctly configured with the hosts you want to manage.

    ```ini
    [servers]
    your_server_ip ansible_user=your_ssh_user
    ```

2.  **Variables**: Customize the `vars/log_analysis.yml` file to define log files to parse and keywords to search for.

    ```yaml
    # vars/log_analysis.yml
    log_files_to_parse:
      - /var/log/syslog
      - /var/log/auth.log

    keywords_to_find:
      - ERROR
      - WARNING
      - "failed login"
      - "permission denied"
    ```

3.  **Run the Playbook**: Execute the playbook using the `ansible-playbook` command.

    ```bash
    ansible-playbook -i inventory.ini log_parser.yml
    ```

## Output

The playbook will output a summary of the log entries found on the target hosts, highlighting the specified keywords. The output will be displayed on your control machine.

## Extending the Playbook

*   **Custom Modules**: For more complex parsing, consider writing custom Ansible modules in Python.
*   **Reporting**: Integrate with reporting tools or send notifications (e.g., email, Slack) based on the parsed logs.
*   **Time-based Analysis**: Add logic to filter logs within a specific time range.
