# Nightly Survival Service Sentinel

This Ansible playbook acts as a vigilant sentinel, monitoring the operational status of critical system services and ensuring the presence of essential configuration files across your infrastructure. It generates a 'Sentinel's Log' report, providing a quick overview of your systems' readiness.

## Features

*   **Service Status Check**: Verifies if specified critical services are running.
*   **Configuration File Presence**: Confirms that vital configuration files exist on the target hosts.
*   **Comprehensive Reporting**: Generates a detailed log file for each host, indicating overall status (NOMINAL or ALERT) and specifics for each checked item.
*   **Whimsical yet Useful**: Keeps your post-apocalyptic infrastructure in check with a touch of thematic flair.

## Usage

1.  **Inventory**: Update the `src/inventory.ini` file with the hosts you wish to monitor. Ensure Ansible can connect to these hosts (e.g., via SSH).

    ```ini
    [sentinels]
    server1.example.com
    server2.example.com
    # ... add your critical servers here
    ```

2.  **Define Critical Services/Configs**: Modify `vars/survival_services.yml` to list the services and configuration files relevant to your 'survival' infrastructure.

    ```yaml
    critical_services:
      - name: sshd
      - name: systemd-journald
      - name: cron

    critical_config_files:
      - path: /etc/ssh/sshd_config
      - path: /etc/fstab
      - path: /etc/crontab
    ```

3.  **Run the Playbook**: Execute the playbook using `ansible-playbook`.

    ```bash
    ansible-playbook -i src/inventory.ini src/sentinel_playbook.yml
    ```

    The playbook will generate a report for each host in `/tmp/sentinel_reports/` on the Ansible control node.

## Testing

To ensure the playbook's logic works correctly without interacting with actual services or files on a live system, a dedicated test playbook is provided. This test playbook uses mocked facts to simulate different system states (nominal and alert).

To run the tests:

```bash
ansible-playbook -i src/inventory.ini tests/test_sentinel_playbook.yml
```

This will execute two test cases:

1.  **Nominal Case**: Simulates all services running and all configuration files present, asserting that the overall status is `NOMINAL`.
2.  **Alert Case**: Simulates a stopped service and a missing configuration file, asserting that the overall status is `ALERT` and identifying the specific issues.

Each test run will generate a temporary report file in `/tmp/sentinel_reports/` (e.g., `test-host-nominal_sentinel_log_20231027T220000.txt`) and then clean it up.
