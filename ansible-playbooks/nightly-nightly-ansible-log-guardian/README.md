# Nightly Ansible Log Guardian

This Ansible playbook, the "Log Guardian," is designed to automate the configuration and management of log rotation for critical system logs across your fleet of servers. In the post-apocalyptic landscape, every byte of disk space is precious, and ensuring logs don't consume vital resources while still preserving historical data for anomaly detection is paramount.

The Log Guardian ensures your logs are rotated, compressed, and eventually removed according to your specified policies, keeping your systems lean and operational.

## Features

*   **Automated Logrotate Configuration**: Deploys custom `logrotate` configuration files for specified log paths.
*   **Compression**: Configures log compression to save disk space.
*   **Retention Policy**: Allows defining how many rotated logs to keep.
*   **Service Reload**: Ensures `logrotate` service is aware of new configurations.

## Prerequisites

*   Ansible installed on your control machine.
*   SSH access to target servers with `sudo` privileges.
*   Target servers should be running a Linux distribution with `logrotate` available (e.g., Debian/Ubuntu, RHEL/CentOS).

## Usage

1.  **Define your inventory**:
    Edit `src/inventory.ini` to list your target servers.

    ```ini
    [servers]
    your_server_1 ansible_host=192.168.1.10
    your_server_2 ansible_host=192.168.1.11
    localhost ansible_connection=local
    ```

2.  **Configure log rotation parameters**:
    Edit `src/vars/main.yml` to specify the log files to manage and their rotation policies.

    ```yaml
    ---
    log_guardian_configs:
      - name: "shelter_sentry_logs"
        path: "/var/log/shelter/*.log"
        frequency: daily
        rotate: 7
        compress: yes
        delaycompress: yes
        missingok: yes
        notifempty: yes
        create: "0640 root adm"
        postrotate: "/usr/bin/systemctl reload rsyslog > /dev/null 2>&1 || true"
      - name: "temporal_anomaly_logs"
        path: "/var/log/temporal_anomalies.log"
        frequency: weekly
        rotate: 4
        compress: yes
        missingok: yes
        notifempty: yes
        create: "0600 root root"
    ```
    *   `name`: A unique identifier for the log configuration.
    *   `path`: The glob pattern for log files to rotate.
    *   `frequency`: `daily`, `weekly`, `monthly`, `yearly`.
    *   `rotate`: Number of rotated logs to keep.
    *   `compress`: `yes` or `no`.
    *   `delaycompress`: `yes` or `no`.
    *   `missingok`: `yes` or `no`.
    *   `notifempty`: `yes` or `no`.
    *   `create`: Permissions and owner/group for new log files (e.g., "0640 root adm").
    *   `postrotate`: Commands to run after rotation (optional).

3.  **Run the playbook**:

    ```bash
    ansible-playbook -i src/inventory.ini src/log_guardian.yml
    ```

    For a dry run:
    ```bash
    ansible-playbook -i src/inventory.ini src/log_guardian.yml --check --diff
    ```

## Testing

The playbook includes a self-contained test suite to verify its syntax and the correct deployment of `logrotate` configurations.

To run the tests:

```bash
ansible-playbook -i src/inventory.ini tests/test_log_guardian.yml
```

This will execute the main playbook against `localhost` (as defined in `src/inventory.ini`) and then assert that the `logrotate` configuration files are created correctly with the expected content.
