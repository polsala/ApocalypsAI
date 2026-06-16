# Nightly Chrono-Sync Beacon

The ApocalypsAI Nightly Integrator presents the "Chrono-Sync Beacon" – a whimsical yet vital Ansible playbook designed to ensure your infrastructure remains temporally stable and operationally sound amidst the cosmic chaos. This beacon will synchronize system clocks, verify the health of critical services, and monitor disk space to prevent any unexpected "reality distortions."

## Features

*   **Temporal Alignment**: Ensures all target systems are synchronized with specified NTP servers.
*   **Service Stability Check**: Verifies that essential services are running as expected.
*   **Spatial Integrity Monitor**: Checks disk space utilization to prevent critical storage overloads.
*   **Comprehensive Reporting**: Provides a summary of the temporal and operational status of your hosts.

## Usage

1.  **Prerequisites**:
    *   Ansible installed on your control machine.
    *   SSH access to your target hosts with appropriate permissions (e.g., `sudo` privileges for time synchronization and service management).

2.  **Inventory Setup**:
    Create an `inventory.ini` file (or use the provided `src/inventory.ini` as a template) listing your target hosts.

    ```ini
    [chronos_servers]
    server1.example.com
    server2.example.com ansible_user=ubuntu
    ```

3.  **Configuration**:
    Review and modify the variables in `src/vars/main.yml` to suit your environment:
    *   `ntp_servers`: List of NTP servers for synchronization.
    *   `critical_services`: List of service names to monitor (e.g., `nginx`, `postgresql`).
    *   `disk_threshold_percent`: Percentage threshold for disk space alerts (e.g., 85).

4.  **Run the Beacon**:
    Execute the playbook from the `nightly-chrono-sync-beacon` directory:

    ```bash
    ansible-playbook -i src/inventory.ini src/chrono_sync_beacon.yml
    ```

    To perform a dry run without making changes (highly recommended for initial testing):

    ```bash
    ansible-playbook -i src/inventory.ini src/chrono_sync_beacon.yml --check
    ```

## Example `src/vars/main.yml`

```yaml
# src/vars/main.yml
ntp_servers:
  - 0.pool.ntp.org
  - 1.pool.ntp.org

critical_services:
  - sshd
  - systemd-journald

disk_threshold_percent: 85 # Alert if disk usage exceeds this percentage
```

## Testing

The utility includes a self-contained test playbook `tests/test_chrono_sync_beacon.yml` that uses `localhost` and mocked facts to simulate various scenarios.

To run tests:

```bash
ansible-playbook -i tests/inventory_test.ini tests/test_chrono_sync_beacon.yml
```

This will run the main playbook in `check_mode` against a mock environment and assert expected outcomes without actual system modifications.
