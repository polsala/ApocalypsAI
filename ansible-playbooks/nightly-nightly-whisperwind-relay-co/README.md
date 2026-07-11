# Nightly Whisperwind Relay Config

This Ansible playbook configures and ensures the operational status of Whisperwind Communication Relays. These relays are crucial for broadcasting vital messages, survival tips, and morale-boosting whispers across the desolate wasteland.

## Features

*   Installs necessary relay software (e.g., a simple web server for broadcasting).
*   Configures the relay's broadcast message and port.
*   Ensures the relay service is running and enabled.
*   Generates a status report for all configured relays.

## Requirements

*   Ansible (version 2.9 or higher recommended)
*   Target hosts accessible via SSH with `sudo` privileges.

## Usage

1.  **Define your inventory:**
    Create an `inventory.ini` file specifying your relay hosts.

    ```ini
    [whisperwind_relays]
    relay1.example.com
    relay2.example.com
    ```

2.  **Configure relay variables (optional):**
    You can override default variables in `vars/main.yml` or pass them via the command line.

    ```yaml
    # vars/main.yml
    relay_port: 8080
    broadcast_message: "Hope flickers, even in the darkest night. Stay vigilant, survivors!"
    ```

3.  **Run the playbook:**

    ```bash
    ansible-playbook -i src/inventory.ini src/relay_config.yml
    ```

    To generate a detailed report after running:

    ```bash
    ansible-playbook -i src/inventory.ini src/relay_config.yml --tags "report"
    ```

## Automated Tests

The `tests/test_relay_config.yml` playbook performs a syntax check and a dry run (`--check --diff`) to ensure the playbook is well-formed and would attempt the expected changes without actually applying them.

To run the tests:

```bash
ansible-playbook -i tests/inventory_test.ini tests/test_relay_config.yml
```

This test playbook uses a mock inventory and `ansible_facts` to simulate a target environment without requiring actual remote hosts.
