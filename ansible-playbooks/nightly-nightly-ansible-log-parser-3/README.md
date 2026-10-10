## Nightly Ansible Log Parser

This utility provides an Ansible playbook designed to parse system logs, identify common error patterns, and generate a summary report. It's useful for quickly assessing the health of systems by highlighting potential issues.

### Features

*   Parses common log files (e.g., `/var/log/syslog`, `/var/log/auth.log`).
*   Identifies keywords like 'ERROR', 'WARN', 'FAIL', 'DENIED'.
*   Generates a summary report of found issues.

### Usage

1.  Ensure you have Ansible installed.
2.  Create an inventory file (e.g., `inventory.ini`) specifying the target hosts.
3.  Run the playbook:
    ```bash
    ansible-playbook -i inventory.ini src/parse_logs.yml
    ```

### Customization

*   Modify `vars/main.yml` to change log file paths, keywords to search for, or the output report format.
*   Add new tasks to handle specific log formats or services.

### Testing

This playbook includes a basic test case using `molecule` (though not fully implemented in this standalone example, the structure is provided). For a real-world scenario, you would use `molecule` to test against a defined environment.

For this standalone example, we'll simulate the log parsing by using a mock file and checking the output of the `debug` task.
