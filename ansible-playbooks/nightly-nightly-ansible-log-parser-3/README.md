An Ansible playbook designed to parse system logs, identify common error patterns, and generate a summary report.

## Purpose

This playbook automates the process of sifting through system logs (e.g., `/var/log/syslog`, `/var/log/auth.log`) to pinpoint recurring errors, warnings, and other significant events. It aims to provide a quick, digestible overview of system health from a logging perspective.

## Features

*   Parses specified log files.
*   Identifies common error keywords (e.g., 'error', 'failed', 'warning', 'denied').
*   Counts occurrences of identified log entries.
*   Generates a summary report with the most frequent issues.

## Usage

1.  **Inventory File (`inventory.ini`)**: Ensure your `inventory.ini` file correctly lists the target hosts where logs reside.

    ```ini
    [log_servers]
    your_server_ip_or_hostname
    ```

2.  **Playbook Execution**: Run the playbook using `ansible-playbook`.

    ```bash
    ansible-playbook -i inventory.ini src/parse_logs.yml
    ```

3.  **Output**: The playbook will output a summary of the most frequent log entries to the console. For more detailed analysis, you can modify the `templates/log_summary.j2` to generate a more comprehensive report.

## Customization

*   **Log Files**: Modify the `log_files` variable in `src/parse_logs.yml` to include or exclude specific log paths.
*   **Keywords**: Adjust the `error_keywords` variable in `src/parse_logs.yml` to tailor the search for specific error types.
*   **Reporting**: Enhance the `templates/log_summary.j2` Jinja2 template for more sophisticated reporting formats (e.g., CSV, JSON).

## Testing

This playbook includes basic tests using Ansible's `assert` module to verify that the log parsing and counting tasks execute as expected. These tests are designed to be deterministic and run offline by mocking file content.

To run the tests:

```bash
ansible-playbook -i tests/test_inventory.ini tests/test_parse_logs.yml
```
