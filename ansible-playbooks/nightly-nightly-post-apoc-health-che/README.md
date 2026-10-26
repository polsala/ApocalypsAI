# Nightly Post-Apocalyptic Health Check

This Ansible playbook performs essential health checks on your systems to ensure they are prepared for the daily challenges of the post-apocalyptic world. It verifies the status of critical "survival" services and configurations, providing a quick overview of your infrastructure's readiness.

## Features

*   **Secure Comms Relay Check**: Ensures the SSH service is active for secure remote access.
*   **Perimeter Defense Check**: Verifies that a firewall (firewalld or ufw) is active.
*   **Resource Harvester Check**: Confirms the Docker service is running for containerized operations.
*   **Temporal Drift Monitor Check**: Checks if NTP/Chrony service is active to maintain accurate time.
*   **Data Vault Integrity Check**: Ensures a critical data directory exists and has correct permissions.

## Usage

1.  **Prerequisites**:
    *   Ansible installed on your control machine.
    *   SSH access to your target hosts (if not running on localhost).
    *   `sudo` privileges on target hosts for service checks.

2.  **Inventory**:
    Create an `inventory.ini` file (or use the provided `src/inventory.ini` as a template) listing your target hosts.

    ```ini
    [wasteland_servers]
    server1.example.com
    server2.example.com

    [localhost]
    localhost ansible_connection=local
    ```

3.  **Variables**:
    Review and customize the `vars/main.yml` file for specific paths or service names if needed.

    ```yaml
    ---
    data_vault_path: "/opt/apocalypsai_data_vault"
    data_vault_owner: "root"
    data_vault_group: "root"
    data_vault_mode: "0755"
    ```

4.  **Run the Playbook**:
    Execute the playbook against your inventory:

    ```bash
    ansible-playbook -i src/inventory.ini src/health_check.yml
    ```

    To run in check mode (dry run):

    ```bash
    ansible-playbook -i src/inventory.ini src/health_check.yml --check
    ```

## Automated Tests

The `tests/test_health_check.yml` playbook provides deterministic, offline tests for the logic within `health_check.yml`. It uses `set_fact` to mock system states and `assert` to verify expected outcomes.

To run the tests:

```bash
ansible-playbook -i src/inventory.ini tests/test_health_check.yml
```

*(Note: The `src/inventory.ini` is used for simplicity, but the test playbook itself targets `localhost` and mocks facts.)*
