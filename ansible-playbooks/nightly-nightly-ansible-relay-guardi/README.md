# Nightly Ansible Relay Guardian

This Ansible playbook, `nightly-ansible-relay-guardian`, is designed to act as a vigilant sentinel for your critical communication relay services in a post-apocalyptic world (or just a regular server environment). It ensures that essential services like your 'radio_beacon' or 'data_uplink' are always operational, restarting them if they've unexpectedly ceased functioning.

## Features

*   **Service Monitoring**: Checks the status of a predefined list of critical services.
*   **Automated Restart**: If a critical service is found to be in a 'stopped' state, it attempts to restart it and ensures it's enabled to start on boot.
*   **Status Reporting**: Provides detailed status messages for each service, indicating its state and whether a restart was attempted.
*   **Whimsical Naming**: Keeps the spirit of the ApocalypsAI community alive with themed service names.

## Prerequisites

*   **Ansible**: Version 2.9 or higher installed on your control machine.
*   **Target Hosts**: Servers running `systemd` (most modern Linux distributions) where the critical services are expected to run.
*   **SSH Access**: Ansible requires SSH access to the target hosts, with appropriate permissions (e.g., `sudo` access for service management).

## Usage

1.  **Define your Inventory**: Create or update an `inventory.ini` file with your target hosts. For local testing, `localhost` can be used.

    ```ini
    [relay_servers]
    localhost ansible_connection=local
    # server1.example.com
    # server2.example.com
    ```

2.  **Customize Critical Services**: Edit `src/relay_guardian.yml` to modify the `critical_relay_services` variable if your service names differ from the defaults (`radio_beacon`, `data_uplink`, `emergency_broadcast`). These should correspond to actual `systemd` service names (e.g., `radio_beacon.service`).

3.  **Run the Playbook**: Execute the playbook against your inventory.

    ```bash
    ansible-playbook -i inventory.ini src/relay_guardian.yml
    ```

    To run in check mode (simulate changes without making them):

    ```bash
    ansible-playbook -i inventory.ini src/relay_guardian.yml --check
    ```

## Testing

The utility includes a self-contained test playbook (`tests/test_relay_guardian.yml`) that uses mocked `ansible_facts` to simulate service states. This allows for deterministic and offline testing of the playbook's logic.

1.  **Navigate to the utility directory**:

    ```bash
    cd ansible-playbooks/nightly-ansible-relay-guardian
    ```

2.  **Run the test playbook in check mode**: This will simulate the execution and report 'changed' status for tasks that *would* have run.

    ```bash
    ansible-playbook -i src/inventory.ini tests/test_relay_guardian.yml --check
    ```

    The test playbook will output assertions. A successful run will show all assertions passing.

### Mock Rationale:

The tests simulate `ansible_facts.services` using `set_fact` to provide predefined service states (e.g., 'stopped' or 'running'). This allows the test to verify the playbook's conditional logic (when to restart, what to report) without requiring actual services to be present or manipulated on a live system. The `systemd` module, when run in `--check` mode, will report `changed: true` if its `when` condition is met and it *would* have performed an action, enabling verification of restart attempts. Debug messages are registered and asserted against to confirm correct reporting based on the mocked states.
