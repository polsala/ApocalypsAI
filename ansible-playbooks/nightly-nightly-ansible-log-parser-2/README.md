## Nightly Ansible Log Parser

This utility provides an Ansible playbook designed to parse system logs and identify common error patterns. It aims to offer a quick, automated way to get a high-level overview of potential issues on a system.

### Features

*   Parses `/var/log/syslog` (or a configurable log file).
*   Identifies common error keywords (e.g., 'error', 'failed', 'warning', 'critical').
*   Counts occurrences of identified error patterns.
*   Generates a summary report.

### Usage

1.  **Inventory File**: Ensure your `inventory.ini` file is correctly configured with the target hosts.
2.  **Playbook Execution**: Run the playbook using `ansible-playbook -i inventory.ini log_parser.yml`.

### Customization

*   **Log File**: Modify the `log_file_path` variable in `log_parser.yml` to point to your desired log file.
*   **Error Keywords**: Update the `error_keywords` list in `log_parser.yml` to include or exclude specific terms.

### Testing

This playbook includes a basic test case using Ansible's `assert` module to verify that the log parsing task runs without errors and produces output. For more comprehensive testing, consider using Molecule.
