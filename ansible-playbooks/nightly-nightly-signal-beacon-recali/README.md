# Nightly Signal-Beacon Recalibrator

## Overview

In the desolate expanse of the post-apocalyptic world, reliable communication is the lifeline of our scattered communities. The `nightly-signal-beacon-recalibrator` is a crucial Ansible playbook designed to ensure our network of signal beacons remains optimally tuned and operational. It performs essential maintenance tasks, checking for frequency alignment, ensuring vital services are active, and managing "power crystals" and "log crystals" to keep the whispers of hope flowing across the wasteland.

## Features

*   **Frequency Alignment Check**: Verifies and corrects the `beacon_frequency` setting in the beacon's configuration file.
*   **Signal Service Assurance**: Ensures the critical `beacon_signal_service` is running and enabled.
*   **Power Crystal Management**: Confirms the presence of the `/var/lib/beacon/power_crystals` directory, essential for beacon operation.
*   **Log Crystal Rotation**: Performs a basic rotation of the beacon's log file to prevent overflow.

## Usage

1.  **Prerequisites**:
    *   Ansible installed on your control machine.
    *   SSH access to your beacon hosts.
    *   Python 3 on target hosts (for Ansible's remote execution).

2.  **Inventory Setup**:
    Create an `inventory.ini` file (or modify the provided example) listing your beacon hosts.

    ```ini
    [beacons]
    beacon1.example.com
    beacon2.example.com
    ```

3.  **Configuration Variables**:
    Review and adjust variables in `src/vars/main.yml` if needed.

    ```yaml
    beacon_config_path: /etc/beacon/config.ini
    beacon_frequency_key: frequency
    beacon_default_frequency: 42.0
    beacon_signal_service_name: beacon_service
    beacon_power_crystal_dir: /var/lib/beacon/power_crystals
    beacon_log_file: /var/log/beacon/beacon.log
    ```

4.  **Run the Playbook**:
    Execute the playbook using the `ansible-playbook` command:

    ```bash
    ansible-playbook -i src/inventory.ini src/recalibrate_beacons.yml
    ```

    To perform a dry run without making changes:

    ```bash
    ansible-playbook -i src/inventory.ini src/recalibrate_beacons.yml --check
    ```

## Testing

The `tests/test_recalibrate_beacons.yml` playbook provides a way to verify the utility's functionality and idempotency. It uses `localhost` to simulate a beacon environment.

To run the tests:

```bash
ansible-playbook -i tests/inventory_test.ini tests/test_recalibrate_beacons.yml
```

This test playbook will:
1.  Set up a pristine environment on `localhost`.
2.  Run the main playbook and assert changes are made.
3.  Run the main playbook again and assert no further changes (idempotency).
4.  Simulate a drift in configuration.
5.  Run the main playbook and assert it corrects the drift.
