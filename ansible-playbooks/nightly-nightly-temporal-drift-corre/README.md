# Nightly Temporal Drift Corrector

An Ansible playbook to detect and correct temporal drift on servers, ensuring cosmic clock alignment. This utility helps maintain accurate time synchronization across your infrastructure, preventing issues caused by clock skew.

## Features

- Checks the status of the `systemd-timesyncd` NTP service.
- Verifies system clock synchronization using `timedatectl`.
- Automatically starts and enables the NTP service if it's inactive.
- Initiates clock synchronization if the system clock is not synchronized.
- Provides a detailed report of the cosmic clock alignment status.

## Usage

### Prerequisites

- Ansible installed on your control machine.
- SSH access to your target servers with `sudo` privileges.
- `systemd-timesyncd` (or a similar NTP client like `ntp` or `chrony`) installed and configured on target servers. This playbook specifically targets `systemd-timesyncd`.

### Files

- `src/playbook.yml`: The main entry point playbook.
- `src/temporal_drift_tasks.yml`: Contains the core logic for checking and correcting temporal drift.
- `src/inventory.ini`: An example Ansible inventory file.

### Running the Playbook

1.  **Configure your inventory:**
    Edit `src/inventory.ini` to list your target servers. For local execution, `localhost` is pre-configured.

    ```ini
    [servers]
    localhost ansible_connection=local
    # my_server_group
    #   server1.example.com
    #   server2.example.com
    ```

2.  **Run the playbook:**
    Execute the main playbook from the utility's root directory:

    ```bash
    ansible-playbook -i src/inventory.ini src/playbook.yml
    ```

    To run in check mode (dry run) to see what changes *would* be made:

    ```bash
    ansible-playbook -i src/inventory.ini src/playbook.yml --check
    ```

## Testing

Automated tests are provided to ensure the playbook behaves as expected under different scenarios without requiring actual system modifications.

### Running Tests

1.  Navigate to the utility's root directory.
2.  Execute the test playbook:

    ```bash
    ansible-playbook -i tests/inventory_test.ini tests/test_temporal_drift_corrector.yml
    ```

    The `tests/inventory_test.ini` file simply points to `localhost` for test execution.

### Test Scenarios

The `test_temporal_drift_corrector.yml` playbook covers the following scenarios:

-   **Scenario 1: NTP service stopped and unsynced:** Asserts that the playbook would attempt to start the NTP service and synchronize the clock.
-   **Scenario 2: NTP service running but unsynced:** Asserts that the playbook would attempt to synchronize the clock, but not restart the already running NTP service.
-   **Scenario 3: NTP service running and synced (no drift):** Asserts that the playbook would make no changes to a healthy system.

These tests use Ansible's `set_fact` module to mock system command outputs (`systemctl is-active` and `timedatectl status`) and run the core logic in `check_mode` to verify the intended actions.
