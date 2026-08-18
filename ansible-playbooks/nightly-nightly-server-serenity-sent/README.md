# Nightly Server Serenity Sentinel

## Summary
This Ansible playbook acts as a 'Serenity Sentinel' for your servers, performing essential health checks and tidying tasks. It monitors key system metrics (disk, memory, CPU), verifies critical service statuses, and cleans up old log files. Finally, it compiles a comprehensive 'Serenity Report' to give you a snapshot of your server's well-being.

## How it Works
1.  **System Fact Gathering**: Collects basic system information.
2.  **Resource Monitoring**: Checks disk usage, memory consumption, and CPU load.
3.  **Service Verification**: Monitors a configurable list of critical services to ensure they are running.
4.  **Log Tidying**: Identifies and deletes log files older than a specified retention period in configured paths.
5.  **Report Generation**: Compiles all findings into a human-readable 'Serenity Report' saved locally on each target server.

## Usage

### Prerequisites
*   Ansible installed on your control machine.
*   SSH access to your target servers with a user that has `sudo` privileges.
*   Python installed on target servers (Ansible's default requirement).

### Running the Playbook
1.  **Define your inventory**: Update `src/inventory.ini` with your target servers.
    ```ini
    [servers]
    localhost ansible_connection=local
    # server1.example.com
    # server2.example.com
    ```
2.  **Configure variables**: Adjust `src/vars/main.yml` to specify which services to monitor and which log paths to tidy.
    ```yaml
    services_to_monitor:
      - sshd
      - systemd-journald
      # - nginx

    log_paths_to_tidy:
      - /var/log/app # Example: a custom application log directory
      # - /var/log/nginx

    log_retention_days: 7 # Logs older than 7 days will be deleted
    ```
3.  **Execute the playbook**:
    ```bash
    ansible-playbook -i src/inventory.ini src/serenity_sentinel.yml
    ```

### Report Output
The 'Serenity Report' will be generated on each target server at `/tmp/serenity_report_<hostname>.txt`. The playbook will output the path to this report upon completion.

## Testing
To ensure the Serenity Sentinel is functioning correctly, a dedicated test playbook is provided. It uses `localhost` and mocks system command outputs to provide deterministic and offline testing.

### Running Tests
```bash
ansible-playbook -i tests/inventory_test.ini tests/test_serenity_sentinel.yml
```

This will:
1.  Create a temporary log directory and dummy log files.
2.  Mock `df`, `free`, `uptime`, and `service_facts` outputs.
3.  Run the main `serenity_sentinel.yml` playbook with test configurations.
4.  Assert that the report file is created and contains expected content.
5.  Assert that old log files are deleted and recent ones remain.
6.  Clean up the temporary log directory.
