## Nightly Ansible Log Parser

This utility provides an Ansible playbook designed to parse and summarize log files. It aims to identify common error patterns and provide a concise overview of potential issues within your system logs.

### Features

*   Parses specified log files.
*   Identifies lines containing common error keywords (e.g., ERROR, WARN, CRITICAL).
*   Counts occurrences of identified error patterns.
*   Generates a summary report.

### Usage

1.  **Inventory File (`inventory.ini`)**: Define the hosts you want to run the playbook on.
    ```ini
    [log_servers]
    your_server_ip_or_hostname
    ```

2.  **Playbook (`src/log_parser.yml`)**: Configure the `log_files_to_parse` variable to specify which log files to analyze.

3.  **Run the Playbook**: Execute the playbook using `ansible-playbook`.
    ```bash
    ansible-playbook -i inventory.ini src/log_parser.yml
    ```

### Customization

*   **`log_files_to_parse`**: A list of absolute paths to the log files you wish to analyze.
*   **`error_keywords`**: A list of keywords to search for within log lines. The playbook defaults to common error indicators.
*   **`report_output_path`**: The local path where the summary report will be saved.

### Testing

Automated tests are included to verify the playbook's functionality using mock data.

Run tests with:
```bash
ansible-playbook tests/test_log_parser.yml
```
