An Ansible playbook designed to parse system logs, identify common error patterns, and generate a summary report.

## Features

*   Parses logs from specified directories.
*   Identifies common error keywords (e.g., ERROR, WARN, CRITICAL).
*   Counts occurrences of identified errors.
*   Generates a summary report with error counts.

## Usage

1.  **Inventory Setup**: Ensure your `inventory.ini` file correctly lists the hosts you want to run this playbook on.

    ```ini
    [log_servers]
    your_server_ip_or_hostname
    ```

2.  **Playbook Execution**: Run the playbook using `ansible-playbook`.

    ```bash
    ansible-playbook -i inventory.ini parse_logs.yml
    ```

    You can specify the log directory to parse using the `log_directory` variable:

    ```bash
    ansible-playbook -i inventory.ini parse_logs.yml --extra-vars "log_directory=/var/log"
    ```

## Customization

*   **`log_directory`**: The directory containing the logs to parse. Defaults to `/var/log`.
*   **`error_patterns`**: A list of regular expressions to identify error messages. You can extend this list in `vars/main.yml`.
*   **`report_output_path`**: The path where the summary report will be saved on the control node. Defaults to `./log_summary_report.txt`.

## Testing

This playbook includes basic tests using `ansible-test` (or manual verification) to ensure the core logic functions as expected. The tests mock the file system to simulate log files and verify the output of the log parsing tasks.
