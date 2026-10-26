# Nightly Server Mood Monitor

This Ansible playbook helps you keep an eye on your servers' "mood" by monitoring key health metrics like CPU, memory, and disk usage. If a server is feeling "grumpy" (metrics exceed defined thresholds) or "sleepy" (critical low resources), it will be reported!

## Features

*   **CPU Load Monitoring**: Checks average CPU load.
*   **Memory Usage Monitoring**: Checks available memory.
*   **Disk Space Monitoring**: Checks free disk space on specified mounts.
*   **Customizable Thresholds**: Define what constitutes "grumpy" or "sleepy" in `vars/mood_thresholds.yml`.
*   **Detailed Mood Report**: Generates a human-readable report for each host.

## Usage

1.  **Define your inventory**:
    Create an `src/inventory.ini` file listing your target servers.

    ```ini
    [servers]
    your_server_1 ansible_host=192.168.1.10
    your_server_2 ansible_host=192.168.1.11
    ```

2.  **Customize Mood Thresholds**:
    Edit `vars/mood_thresholds.yml` to set your desired thresholds.

    ```yaml
    # vars/mood_thresholds.yml
    cpu_load_threshold: 2.0 # Average load over 1 minute
    memory_free_threshold_mb: 512 # Minimum free memory in MB
    disk_free_threshold_percent: 10 # Minimum free disk space percentage
    ```

3.  **Run the Playbook**:
    Execute the playbook using `ansible-playbook`.

    ```bash
    ansible-playbook -i src/inventory.ini src/mood_monitor.yml
    ```

    The playbook will output a mood report for each server directly to the console.

## Automated Tests

The tests simulate different server states (happy, grumpy CPU, sleepy disk) using Ansible's `set_fact` module to override system facts. The tests then assert that the `server_mood`, `mood_details`, and `rendered_mood_report` variables contain expected values based on the mocked facts.

To run the tests:

```bash
ansible-playbook -i tests/inventory_test.ini tests/test_mood_monitor.yml
```

## Directory Structure

```
.
├── README.md
├── src/
│   ├── mood_monitor.yml
│   └── inventory.ini
├── vars/
│   └── mood_thresholds.yml
├── templates/
│   └── mood_report.j2
└── tests/
    ├── test_mood_monitor.yml
    └── inventory_test.ini
```
