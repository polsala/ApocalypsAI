## Nightly Ansible Log Parser

This utility provides an Ansible playbook designed to parse system logs, identify common error patterns, and generate a summary report. It's useful for quickly assessing the health of systems by highlighting potential issues.

### Features

*   Parses `/var/log/syslog` (or a configurable log file).
*   Identifies common error keywords (e.g., 'error', 'failed', 'warning', 'critical').
*   Counts occurrences of identified errors.
*   Generates a summary report.

### Usage

1.  **Inventory File (`inventory.ini`)**: Ensure your `inventory.ini` file is correctly configured with the hosts you want to manage.

    ```ini
    [servers]
    your_server_ip_or_hostname ansible_user=your_ssh_user
    ```

2.  **Playbook Execution**: Run the playbook using `ansible-playbook`.

    ```bash
    ansible-playbook -i inventory.ini src/parse_logs.yml
    ```

    You can also specify a different log file path using the `log_file_path` variable:

    ```bash
    ansible-playbook -i inventory.ini src/parse_logs.yml --extra-vars "log_file_path=/var/log/messages"
    ```

### Customization

*   **`error_keywords`**: Modify the `vars/main.yml` file to add or remove keywords to search for in the logs.
*   **`log_file_path`**: Change the default log file path in `vars/main.yml` or pass it as an `--extra-vars` argument.

### Testing

This playbook includes a basic test using `molecule` (though the provided test is a simplified mock for demonstration purposes). To run the tests:

```bash
cd tests
molecule test
```

### License

This project is licensed under the MIT License - see the `LICENSE` file for details.
