An Ansible playbook designed to parse and summarize system logs. It identifies common error and warning patterns, providing a concise overview of potential issues on managed hosts.

## Features

*   Parses `/var/log/syslog` (or a configurable log file).
*   Identifies common error keywords (e.g., ERROR, FAIL, CRITICAL).
*   Identifies common warning keywords (e.g., WARNING, WARN).
*   Generates a summary report of found errors and warnings.

## Usage

1.  **Inventory Setup**: Ensure your `inventory.ini` file is correctly configured with the hosts you want to manage.
2.  **Run the Playbook**: Execute the playbook using `ansible-playbook -i inventory.ini parse_logs.yml`.

## Customization

*   **Log File**: Modify the `log_file_path` variable in `vars/main.yml` to point to a different log file.
*   **Keywords**: Update the `error_keywords` and `warning_keywords` lists in `vars/main.yml` to customize what patterns are searched for.

## Testing

This playbook includes a basic test case that mocks the log file content and verifies the output of the log parsing task.
