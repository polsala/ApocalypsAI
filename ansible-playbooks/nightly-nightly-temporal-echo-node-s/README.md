# Nightly Temporal Echo Node Stabilizer

## Overview

This Ansible playbook, `nightly-temporal-echo-node-stabil`, is designed to maintain the stability and operational integrity of distributed "Temporal Echo Nodes." These nodes are crucial for localized temporal anomaly stabilization, ensuring that their core services are running, configurations are consistent, and log files are properly managed.

## Features

*   **Service Health Assurance**: Ensures the `temporal-echo-service` is running and enabled on all target nodes.
*   **Configuration Integrity**: Deploys a standardized configuration file (`echo_service.conf`) from a Jinja2 template, ensuring all nodes adhere to the desired operational parameters.
*   **Log Management**: Sets up `logrotate` configurations to prevent log files from consuming excessive disk space, ensuring continuous operation.
*   **Idempotent Operations**: All tasks are designed to be idempotent, meaning they can be run multiple times without causing unintended side effects or making changes if the system is already in the desired state.

## Usage

1.  **Prerequisites**:
    *   Ansible installed on your control machine.
    *   SSH access to your target "Temporal Echo Nodes" (or `ansible_connection=local` for local testing).
    *   `sudo` privileges on the target nodes for service and file management.

2.  **Inventory**: Update the `src/inventory.ini` file with the hostnames or IP addresses of your Temporal Echo Nodes. For local testing, `localhost` is pre-configured.

    ```ini
    [echo_nodes]
    localhost ansible_connection=local
    # node1.example.com
    # node2.example.com
    ```

3.  **Variables**: Review and adjust the variables in `src/vars/main.yml` to match your desired service name, configuration paths, and operational parameters.

    ```yaml
    echo_service_name: temporal-echo-service
    echo_config_path: /etc/temporal-echo/echo_service.conf
    echo_log_path: /var/log/temporal-echo/service.log
    echo_stabilization_frequency: 60 # seconds
    echo_power_level: "standard" # or "boosted", "minimal"
    ```

4.  **Run the Playbook**:

    Navigate to the utility's root directory and execute the playbook:

    ```bash
    ansible-playbook -i src/inventory.ini src/stabilize_nodes.yml
    ```

    To perform a dry run (check what changes *would* be made without actually applying them):

    ```bash
    ansible-playbook -i src/inventory.ini src/stabilize_nodes.yml --check --diff
    ```

## Testing

The `tests/test_stabilize_nodes.yml` playbook provides a comprehensive, offline, and deterministic test suite for the main stabilization playbook. It uses `connection: local` to simulate a target environment and verifies idempotency and drift detection.

To run the tests:

```bash
ansible-playbook -i src/inventory.ini tests/test_stabilize_nodes.yml
```

### Test Scenarios Covered:

1.  **Initial Check Mode**: Verifies that on a fresh system, the playbook correctly identifies and reports changes in `check_mode`.
2.  **Full Run**: Executes the playbook to apply all necessary configurations and service states.
3.  **Idempotency Check**: Runs the playbook again in `check_mode` after a full run, asserting that no further changes are reported, confirming idempotency.
4.  **Configuration Drift Detection**: Introduces a simulated configuration drift and then runs the playbook in `check_mode` to ensure it correctly detects the discrepancy.

### Mock Rationale for Tests:

*   **Service Module Mocking**: A dummy systemd unit file for `temporal-echo-service` is created in `/etc/systemd/system/` to allow the `ansible.builtin.service` module to operate without requiring a real, complex service. This enables testing the *logic* of service management (started, enabled) and its `changed` status without actual service daemon interactions.
*   **File System Mocking**: Temporary directories and files are used (`/tmp/ansible_test_echo_node`, `/etc/temporal-echo/`) to simulate the target file system, allowing for deterministic testing of `ansible.builtin.template` and `ansible.builtin.copy` modules.
*   **Idempotency and Drift**: Ansible's `check_mode` and `diff` capabilities are leveraged to verify that tasks only report changes when necessary and can detect when a system deviates from the desired state. This is a core feature of Ansible's testing methodology for configuration management.
