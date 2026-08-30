# Nightly Ansible Service Mood Monitor

This Ansible playbook monitors a list of critical system services. If a service is found to be in a non-active state (e.g., stopped or failed), the playbook attempts to restart it. After checking or restarting, it reports the service's 'mood' (status) in a whimsical manner.

## Features

*   **Service Monitoring**: Checks the `ActiveState` of specified systemd services.
*   **Automatic Restart**: Attempts to restart services that are not `active`.
*   **Whimsical Mood Reporting**: Provides a fun, human-readable status for each service.
*   **Configurable**: Easily add or remove services to monitor via `vars/service_config.yml`.

## Prerequisites

*   **Ansible**: Installed on the control node.
*   **Target Hosts**: Must be running `systemd` as their service manager.
*   **SSH Access**: The Ansible control node needs SSH access to the target hosts with appropriate permissions (`become: yes` is used for `systemd` operations).

## Usage

1.  **Clone the repository** (or copy this utility's folder).

2.  **Configure your inventory**: Edit `src/inventory.ini` to list your target servers. For local testing, `localhost` is pre-configured.

    ```ini
    # src/inventory.ini
    [servers]
    localhost ansible_connection=local
    # server1.example.com
    # server2.example.com
    ```

3.  **Configure critical services**: Edit `src/vars/service_config.yml` to specify which services to monitor.

    ```yaml
    # src/vars/service_config.yml
    critical_services:
      - name: "nginx"
        description: "Web Server"
      - name: "postgresql"
        description: "Database Server"
      - name: "sshd"
        description: "Secure Shell Daemon"
    # ... add more services as needed

    service_moods:
      active: "Chirping merrily 🐦"
      inactive: "Slumbering peacefully 😴"
      failed: "Grumpy and unresponsive 😠"
      activating: "Stretching awake ✨"
      deactivating: "Winding down ⏳"
      reloading: "Taking a deep breath 💨"
      unknown: "Lost in the void 🌌"
    ```

4.  **Run the playbook**:

    ```bash
    ansible-playbook -i src/inventory.ini src/service_mood_monitor.yml
    ```

    Ansible will connect to your specified hosts, check the status of each critical service, attempt to restart any non-active ones, and then report their final 'mood'.

## Testing

To run the automated tests for this utility:

```bash
ansible-playbook -i tests/inventory_test.ini tests/test_service_mood_monitor.yml --syntax-check
ansible-playbook -i tests/inventory_test.ini tests/test_service_mood_monitor.yml
```

The test playbook will create a dummy systemd service, manipulate its state, run the main `service_mood_monitor.yml` against it, and assert that the service's state is correctly managed.
