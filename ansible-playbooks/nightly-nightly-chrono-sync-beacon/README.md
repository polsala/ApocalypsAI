# Nightly Chrono-Sync Beacon

This Ansible playbook ensures temporal consistency across your fleet of servers by synchronizing their system clocks using NTP or Chrony. In the chaotic post-apocalyptic landscape, accurate timekeeping is crucial for log correlation, security, and the reliable operation of distributed systems.

## Features

*   Installs and configures `ntp` or `chrony` (configurable).
*   Sets up specified NTP servers for synchronization.
*   Ensures the time synchronization service is running and enabled.
*   Provides an option to force an immediate time sync.
*   Reports the current system time and synchronization status.

## Prerequisites

*   **Ansible**: Installed on your control machine.
*   **Target Hosts**: Servers accessible via SSH from your control machine, with Python installed (Ansible's default connection method).
*   **Sudo Access**: The Ansible user on target hosts needs `sudo` privileges to install packages and modify system configurations.

## Usage

1.  **Define your inventory**: Create an `inventory.ini` file or update an existing one with your target hosts.

    ```ini
    [chronosynced_servers]
    server1.example.com
    server2.example.com
    192.168.1.10
    ```

2.  **Configure variables**: Review and modify `vars/main.yml` to specify your preferred time synchronization package (`ntp` or `chrony`) and the list of NTP servers.

    ```yaml
    # vars/main.yml
    ---
    time_sync_package: "ntp" # or "chrony"
    ntp_servers:
      - 0.pool.ntp.org
      - 1.pool.ntp.org
      - 2.pool.ntp.org
    force_time_sync: true # Set to false to only configure and start service
    ```

3.  **Run the playbook**: Execute the playbook from your control machine.

    ```bash
    ansible-playbook -i inventory.ini chrono_sync_beacon.yml
    ```

    Add `-b` or `--become` if your user needs to escalate privileges on the remote host (which is usually the case for system-level changes).

    ```bash
    ansible-playbook -i inventory.ini chrono_sync_beacon.yml --become
    ```

## Testing

To run the deterministic, offline tests for this utility:

```bash
ansible-playbook -i tests/inventory_test.ini tests/test_chrono_sync_beacon.yml
```

This will create mock files on your local machine to simulate the installation and configuration, then assert their content and existence.
