# Nightly Signal Scavenger

## Overview

The `nightly-signal-scavenger` is an Ansible playbook designed to monitor the health and availability of distributed "signal beacons" and "data fragments" across your post-apocalyptic network. It helps ensure that critical communication channels are open and vital data caches are intact, providing a consolidated status report.

## Features

*   **Beacon Connectivity Check**: Pings designated hosts (beacons) to verify network reachability.
*   **Data Fragment Verification**: Checks for the existence of specified data files or directories (data fragments) on each beacon.
*   **Status Reporting**: Generates a detailed, human-readable report summarizing the status of all monitored beacons and their data fragments.

## Requirements

*   Ansible (version 2.9 or higher recommended)
*   Python 3 on the control node and target hosts (if `ansible_connection=ssh` is used)

## Usage

1.  **Define your Beacons**: Edit the `inventory.ini` file to list your target hosts (beacons) and define variables like `beacon_id` and `data_path` for each.

    ```ini
    [beacons]
    beacon_alpha ansible_host=127.0.0.1 ansible_connection=local beacon_id=ALPHA data_path=/tmp/signal_data/alpha.txt
    beacon_beta ansible_host=127.0.0.1 ansible_connection=local beacon_id=BETA data_path=/tmp/signal_data/beta.txt
    # For remote hosts, use:
    # remote_beacon ansible_host=your.remote.ip ansible_user=your_user beacon_id=REMOTE data_path=/path/to/remote/data.txt
    ```

2.  **Run the Scavenger Playbook**: Execute the main playbook.

    ```bash
    ansible-playbook -i inventory.ini scavenger_playbook.yml
    ```

3.  **Review the Report**: A `signal_scavenger_report.txt` file will be generated in the directory where the playbook is run, containing the status summary.

## Testing

To run the automated tests, ensure you have Ansible installed, then execute the test playbook:

```bash
ansible-playbook -i tests/inventory_test.ini tests/test_scavenger_playbook.yml
```

This will create temporary files, run the main playbook against a local test environment, verify the report, and clean up afterwards.
