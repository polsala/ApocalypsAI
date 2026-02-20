# Nightly Cosmic Clock Aligner

## Overview

The `nightly-cosmic-clock-aligner` is an Ansible playbook designed to bring your system clocks into perfect temporal harmony with the universe's celestial timekeepers. It ensures that all your managed nodes are synchronized using the Network Time Protocol (NTP), specifically leveraging `chrony` for robust and precise timekeeping.

Because in the post-apocalyptic world, knowing the exact time is crucial for coordinating scavenger runs, scheduling broadcasts, and avoiding temporal anomalies.

## Features

*   **`chrony` Installation**: Automatically installs the `chrony` NTP client on target systems.
*   **NTP Configuration**: Configures `chrony` to use a set of reliable NTP pool servers.
*   **Service Management**: Ensures the `chronyd` service is enabled and running.
*   **Idempotent**: Can be run multiple times without making unnecessary changes.
*   **Whimsical**: Infuses a touch of cosmic wonder into mundane time synchronization.

## Usage

1.  **Prerequisites**:
    *   Ansible installed on your control machine.
    *   SSH access to your target nodes with `sudo` privileges.

2.  **Inventory**: Update the `src/inventory.ini` file with your target hosts. For local testing, `localhost` is pre-configured.

    ```ini
    [cosmic_nodes]
    localhost ansible_connection=local
    # server1.example.com
    # server2.example.com
    ```

3.  **Run the Playbook**: Execute the playbook using `ansible-playbook`.

    ```bash
    ansible-playbook -i src/inventory.ini src/align_clocks.yml
    ```

    To target specific hosts (e.g., only `server1.example.com`):

    ```bash
    ansible-playbook -i src/inventory.ini src/align_clocks.yml --limit server1.example.com
    ```

4.  **Customize NTP Servers**: You can modify the `ntp_servers` list in `vars/main.yml` to use your preferred NTP sources.

## Testing

The utility includes a self-contained test playbook (`tests/test_align_clocks.yml`) that verifies the configuration logic in an offline and deterministic manner. It does this by rendering the `chrony.conf` template to a temporary location and asserting its content, without modifying your actual system.

To run the tests:

```bash
ansible-playbook -i src/inventory.ini tests/test_align_clocks.yml
```

This will:
*   Create a temporary directory in your home folder (`~/.ansible_test_temp_config`).
*   Render the `chrony.conf.j2` template into this temporary directory.
*   Read the rendered configuration and assert that it contains the expected NTP server entries and other core `chrony` directives.
*   Clean up the temporary directory.

This ensures that the playbook's configuration generation is correct, even without a live `chrony` service or network access.
