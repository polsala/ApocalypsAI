## Nightly Ansible Log Harmonizer

This utility provides an Ansible playbook designed to standardize log formats across a fleet of servers. By ensuring consistent log structures, it significantly simplifies log aggregation, searching, and analysis, especially in a post-apocalyptic environment where every byte of data counts.

### Features

*   **Log Format Standardization**: Applies a chosen log format (e.g., JSON) to specified log files.
*   **Configuration Management**: Manages log rotation and retention policies.
*   **Idempotent**: Can be run multiple times without unintended side effects.
*   **Customizable**: Easily adaptable to different log types and desired formats.

### Prerequisites

*   Ansible installed on the control node.
*   SSH access to target hosts with appropriate privileges.
*   Python installed on target hosts (required by many Ansible modules).

### Usage

1.  **Inventory Setup**: Update the `inventory.ini` file with your target hosts.
2.  **Configuration**: Modify `vars/log_harmonizer_vars.yml` to specify:
    *   `log_files_to_harmonize`: A list of log file paths to process.
    *   `target_log_format`: The desired log format (e.g., `json`, `syslog`).
    *   `log_rotation_enabled`: Whether to enable log rotation.
    *   `log_rotation_interval`: The rotation interval (e.g., `daily`, `weekly`).
    *   `log_rotation_count`: The number of old log files to keep.
3.  **Run the Playbook**: Execute the playbook using the following command:
    ```bash
    ansible-playbook -i inventory.ini log_harmonizer.yml
    ```

### Testing

Automated tests are included to verify the playbook's functionality. Run them using:

```bash
ansible-playbook tests/test_log_harmonizer.yml
```

### License

This project is licensed under the MIT License - see the `LICENSE` file for details.
