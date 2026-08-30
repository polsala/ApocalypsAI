# Nightly Temporal Beacon Keeper

Ensures your critical 'temporal beacons' (servers) maintain accurate time synchronization using NTP, which is vital for coordinating operations in any environment, especially a post-apocalyptic one.

This Ansible playbook checks the status of the `systemd-timesyncd` service (common on modern Linux distributions), ensures it's running and enabled, and reports on the overall time synchronization status of each host.

## Features

*   **Service Management**: Verifies `systemd-timesyncd` is active and configured to start on boot.
*   **Synchronization Check**: Reports whether the system's time is synchronized via NTP.
*   **Status Reporting**: Provides a clear summary for each host.

## Prerequisites

*   **Ansible**: Installed on your control machine.
*   **Target Hosts**: Linux machines with `systemd` and `systemd-timesyncd` (or a compatible NTP client) installed.
*   **SSH Access**: Your Ansible control machine must have SSH access to the target hosts, preferably with passwordless sudo configured.

## Usage

1.  **Inventory File**: Create an `inventory.ini` file (or use an existing one) listing your target hosts. For example:

    ```ini
    [temporal_beacons]
    server1.example.com
    server2.example.com
    ```

2.  **Run the Playbook**: Execute the playbook using `ansible-playbook`:

    ```bash
    ansible-playbook -i inventory.ini src/temporal_beacon_keeper.yml
    ```

    To run against specific hosts or groups:

    ```bash
    ansible-playbook -i inventory.ini src/temporal_beacon_keeper.yml --limit temporal_beacons
    ```

## Example Output

```
PLAY [Ensure Temporal Beacons are Synchronized] ********************************

TASK [Gathering Facts] *********************************************************
ok: [server1.example.com]
ok: [server2.example.com]

TASK [Ensure NTP service (systemd-timesyncd) is running and enabled] ***********
ok: [server1.example.com]
ok: [server2.example.com]

TASK [Get current time synchronization status] *********************************
ok: [server1.example.com]
ok: [server2.example.com]

TASK [Parse time synchronization status] ***************************************
ok: [server1.example.com]
ok: [server2.example.com]

TASK [Report Temporal Beacon Status] *******************************************
ok: [server1.example.com] => {
    "msg": "Host: server1.example.com\nNTP Service (systemd-timesyncd) Active: active\nNTP Service (systemd-timesyncd) Enabled: True\nTime Synchronization Status: Synchronized"
}
ok: [server2.example.com] => {
    "msg": "Host: server2.example.com\nNTP Service (systemd-timesyncd) Active: active\nNTP Service (systemd-timesyncd) Enabled: True\nTime Synchronization Status: Synchronized"
}

PLAY RECAP *********************************************************************
server1.example.com        : ok=5    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
server2.example.com        : ok=5    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
```
